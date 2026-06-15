# 🚀 ScrapeX: Universal Social Media Link Analyzer

## 📌 Overview
ScrapeX is a powerful, hybrid social media data extraction tool built with Python and Streamlit. It intelligently handles anti-bot security using `yt-dlp` and `BeautifulSoup` to extract real-time public data from various social media platforms.

## ✨ Features
- **Universal Compatibility:** Supports YouTube Videos, Facebook Videos, Instagram Reels, and Instagram Photo Posts.
- **Hybrid Extraction Engine:** Automatically switches between media extraction (`yt-dlp`) and meta-tag scraping (`BeautifulSoup`) depending on whether the link is a video or a photo.
- **Smart URL Cleaning:** Automatically extracts valid URLs from messy text inputs or long WhatsApp forwarded messages.
- **Interactive Web UI:** Clean, responsive, and modern interface powered by Streamlit.

## 🛠️ Technologies Used
- Python 3
- Streamlit (Frontend UI)
- yt-dlp (Core Video Data Extraction)
- BeautifulSoup4 & Requests (HTML Meta-tag Scraping)

## 🚀 How to Run Locally

1. **Clone the repository and enter the folder:**
   ```bash
   git clone [https://github.com/smitp3346/social-media-scraper.git](https://github.com/smitp3346/social-media-scraper.git)
   cd social-media-scraper