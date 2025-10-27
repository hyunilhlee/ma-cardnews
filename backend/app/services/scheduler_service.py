"""스케줄러 서비스 - RSS 사이트 자동 크롤링"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime, timedelta
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CrawlScheduler:
    """RSS 크롤링 스케줄러"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler(
            timezone='Asia/Seoul',
            job_defaults={
                'coalesce': True,  # 누적된 작업을 하나로 병합
                'max_instances': 1,  # 동일 작업 중복 실행 방지
                'misfire_grace_time': 300  # 5분 이내 놓친 작업은 실행
            }
        )
        self.scheduler.add_listener(self._job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self._job_registry: Dict[str, Dict] = {}  # site_id -> job info
        logger.info("CrawlScheduler initialized")
    
    def start(self):
        """스케줄러 시작"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started")
    
    def shutdown(self):
        """스케줄러 종료"""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=True)
            logger.info("Scheduler shutdown")
    
    def add_site_job(
        self,
        site_id: str,
        site_name: str,
        rss_url: str,
        crawl_interval: int,
        crawl_func: callable
    ) -> bool:
        """
        사이트 크롤링 작업 등록
        
        Args:
            site_id: 사이트 ID
            site_name: 사이트 이름
            rss_url: RSS 피드 URL
            crawl_interval: 크롤링 주기 (분)
            crawl_func: 크롤링 함수 (site_id를 인자로 받음)
            
        Returns:
            성공 여부
        """
        try:
            job_id = f"crawl_{site_id}"
            
            # 기존 작업이 있으면 제거
            if job_id in self._job_registry:
                self.remove_site_job(site_id)
            
            # 새 작업 등록
            trigger = IntervalTrigger(minutes=crawl_interval)
            job = self.scheduler.add_job(
                func=crawl_func,
                trigger=trigger,
                args=[site_id],
                id=job_id,
                name=f"Crawl: {site_name}",
                replace_existing=True,
                next_run_time=datetime.now() + timedelta(seconds=10)  # 10초 후 첫 실행
            )
            
            # 레지스트리에 등록
            self._job_registry[site_id] = {
                'job_id': job_id,
                'site_name': site_name,
                'rss_url': rss_url,
                'interval': crawl_interval,
                'next_run': job.next_run_time,
                'last_run': None
            }
            
            logger.info(f"Job added: {site_name} (every {crawl_interval} min, next: {job.next_run_time})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add job for site {site_id}: {str(e)}")
            return False
    
    def remove_site_job(self, site_id: str) -> bool:
        """
        사이트 크롤링 작업 제거
        
        Args:
            site_id: 사이트 ID
            
        Returns:
            성공 여부
        """
        try:
            job_id = f"crawl_{site_id}"
            
            if job_id in [job.id for job in self.scheduler.get_jobs()]:
                self.scheduler.remove_job(job_id)
                logger.info(f"Job removed: {job_id}")
            
            if site_id in self._job_registry:
                del self._job_registry[site_id]
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to remove job for site {site_id}: {str(e)}")
            return False
    
    def update_site_job(
        self,
        site_id: str,
        site_name: str,
        rss_url: str,
        crawl_interval: int,
        crawl_func: callable
    ) -> bool:
        """
        사이트 크롤링 작업 업데이트
        
        Args:
            site_id: 사이트 ID
            site_name: 사이트 이름
            rss_url: RSS 피드 URL
            crawl_interval: 크롤링 주기 (분)
            crawl_func: 크롤링 함수
            
        Returns:
            성공 여부
        """
        try:
            job_id = f"crawl_{site_id}"
            
            if job_id in [job.id for job in self.scheduler.get_jobs()]:
                # 기존 작업 제거 후 재등록
                self.remove_site_job(site_id)
            
            return self.add_site_job(site_id, site_name, rss_url, crawl_interval, crawl_func)
            
        except Exception as e:
            logger.error(f"Failed to update job for site {site_id}: {str(e)}")
            return False
    
    def pause_site_job(self, site_id: str) -> bool:
        """
        사이트 크롤링 작업 일시 중지
        
        Args:
            site_id: 사이트 ID
            
        Returns:
            성공 여부
        """
        try:
            job_id = f"crawl_{site_id}"
            self.scheduler.pause_job(job_id)
            logger.info(f"Job paused: {job_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to pause job for site {site_id}: {str(e)}")
            return False
    
    def resume_site_job(self, site_id: str) -> bool:
        """
        사이트 크롤링 작업 재개
        
        Args:
            site_id: 사이트 ID
            
        Returns:
            성공 여부
        """
        try:
            job_id = f"crawl_{site_id}"
            self.scheduler.resume_job(job_id)
            logger.info(f"Job resumed: {job_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to resume job for site {site_id}: {str(e)}")
            return False
    
    def trigger_site_job_now(self, site_id: str) -> bool:
        """
        사이트 크롤링 작업 즉시 실행
        
        Args:
            site_id: 사이트 ID
            
        Returns:
            성공 여부
        """
        try:
            job_id = f"crawl_{site_id}"
            job = self.scheduler.get_job(job_id)
            
            if job:
                # 다음 실행 시간을 현재 시간으로 변경
                job.modify(next_run_time=datetime.now())
                logger.info(f"Job triggered now: {job_id}")
                return True
            else:
                logger.warning(f"Job not found: {job_id}")
                return False
            
        except Exception as e:
            logger.error(f"Failed to trigger job for site {site_id}: {str(e)}")
            return False
    
    def get_job_info(self, site_id: str) -> Optional[Dict]:
        """
        작업 정보 조회
        
        Args:
            site_id: 사이트 ID
            
        Returns:
            작업 정보 또는 None
        """
        try:
            job_id = f"crawl_{site_id}"
            job = self.scheduler.get_job(job_id)
            
            if job:
                return {
                    'job_id': job.id,
                    'name': job.name,
                    'next_run': job.next_run_time,
                    'pending': job.pending
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get job info for site {site_id}: {str(e)}")
            return None
    
    def get_all_jobs(self) -> list:
        """
        모든 작업 목록 조회
        
        Returns:
            작업 목록
        """
        try:
            jobs = []
            for job in self.scheduler.get_jobs():
                jobs.append({
                    'job_id': job.id,
                    'name': job.name,
                    'next_run': job.next_run_time,
                    'pending': job.pending
                })
            return jobs
            
        except Exception as e:
            logger.error(f"Failed to get all jobs: {str(e)}")
            return []
    
    def _job_listener(self, event):
        """
        작업 실행 이벤트 리스너
        
        Args:
            event: 작업 실행 이벤트
        """
        try:
            if event.exception:
                logger.error(f"Job {event.job_id} failed: {event.exception}")
            else:
                logger.info(f"Job {event.job_id} executed successfully")
                
                # 레지스트리 업데이트
                site_id = event.job_id.replace('crawl_', '')
                if site_id in self._job_registry:
                    self._job_registry[site_id]['last_run'] = datetime.now()
                    
                    # 다음 실행 시간 업데이트
                    job = self.scheduler.get_job(event.job_id)
                    if job:
                        self._job_registry[site_id]['next_run'] = job.next_run_time
                        
        except Exception as e:
            logger.error(f"Error in job listener: {str(e)}")


# 전역 스케줄러 인스턴스
_scheduler_instance: Optional[CrawlScheduler] = None


def get_scheduler() -> CrawlScheduler:
    """
    전역 스케줄러 인스턴스 가져오기
    
    Returns:
        CrawlScheduler 인스턴스
    """
    global _scheduler_instance
    
    if _scheduler_instance is None:
        _scheduler_instance = CrawlScheduler()
    
    return _scheduler_instance


def init_scheduler():
    """스케줄러 초기화 및 시작"""
    scheduler = get_scheduler()
    scheduler.start()
    logger.info("Scheduler initialized and started")
    return scheduler


def shutdown_scheduler():
    """스케줄러 종료"""
    global _scheduler_instance
    
    if _scheduler_instance:
        _scheduler_instance.shutdown()
        _scheduler_instance = None
        logger.info("Scheduler shutdown")

