from typing import List, Dict
from pathlib import Path
import json
import config


class LongTailManager:
    def __init__(self):
        self.data_file = config.PROJECT_ROOT / "_data" / "longtail_keywords.json"
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.keywords = self._load()
    
    def _load(self) -> Dict:
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"used": [], "pending": []}
    
    def _save(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.keywords, f, ensure_ascii=False, indent=2)
    
    def add_pending(self, keywords: List[str]):
        for kw in keywords:
            kw_clean = kw.strip().lower()
            if kw_clean and kw_clean not in self.keywords['used'] and kw_clean not in self.keywords['pending']:
                self.keywords['pending'].append(kw_clean)
        self._save()
    
    def get_next(self, count: int = 5) -> List[str]:
        result = self.keywords['pending'][:count]
        return result
    
    def mark_used(self, keywords: List[str]):
        for kw in keywords:
            kw_clean = kw.strip().lower()
            if kw_clean in self.keywords['pending']:
                self.keywords['pending'].remove(kw_clean)
            if kw_clean not in self.keywords['used']:
                self.keywords['used'].append(kw_clean)
        self._save()
    
    def get_stats(self) -> Dict:
        return {
            "total_used": len(self.keywords['used']),
            "total_pending": len(self.keywords['pending']),
            "recent_used": self.keywords['used'][-10:]
        }


def extract_longtail_keywords(sources: List[Dict]) -> List[str]:
    keywords = []
    for source in sources:
        if source.get('source_type') == 'rss':
            title = source.get('title', '')
            if title:
                keywords.append(title[:100])
        elif source.get('source_type') == 'spider':
            title = source.get('title', '')
            if title:
                keywords.append(title[:100])
    return keywords
