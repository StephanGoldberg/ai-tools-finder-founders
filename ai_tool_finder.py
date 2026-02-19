#!/usr/bin/env python3
"""
AI Tools & Founder Resource Finder
Discover trending AI tools for your business and connect with
a community of entrepreneurs who get it.

Powered by:
  → https://aitrend.info       — curated directory of AI tools
  → https://aimomfounders.com  — community for mom entrepreneurs
"""

import urllib.request
import urllib.error
import ssl
import sys
import json
import re
from datetime import datetime


# Categories of AI tools most useful for solo founders and small business owners
TOOL_CATEGORIES = {
    "content": {
        "keywords": ["blog", "write", "copy", "content", "text", "article", "seo"],
        "label": "Content & Writing",
        "description": "AI writing assistants, blog generators, SEO tools",
    },
    "image": {
        "keywords": ["image", "photo", "design", "visual", "logo", "banner", "graphic"],
        "label": "Image & Design",
        "description": "AI image generators and design tools",
    },
    "productivity": {
        "keywords": ["schedule", "task", "email", "automate", "workflow", "manage"],
        "label": "Productivity & Automation",
        "description": "Tools to automate repetitive work",
    },
    "video": {
        "keywords": ["video", "reel", "clip", "edit", "youtube", "tiktok"],
        "label": "Video & Social",
        "description": "AI video creation and editing tools",
    },
    "business": {
        "keywords": ["analytics", "sales", "crm", "marketing", "business", "revenue"],
        "label": "Business & Marketing",
        "description": "AI tools for growth and customer management",
    },
    "code": {
        "keywords": ["code", "develop", "app", "website", "build", "deploy"],
        "label": "No-Code & Development",
        "description": "Build products and automate with AI",
    },
}


def detect_categories(text: str) -> list[str]:
    """Guess which AI tool categories a business might need based on its website."""
    text_lower = text.lower()
    matched = []
    for key, cat in TOOL_CATEGORIES.items():
        if any(kw in text_lower for kw in cat["keywords"]):
            matched.append(key)
    return matched[:3]  # Return top 3 matches


def fetch_url(url: str, timeout: int = 10):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "AIToolFinder/1.0 (https://aitrend.info)"}
    )
    ctx = ssl.create_default_context()
    return urllib.request.urlopen(req, context=ctx, timeout=timeout)


def analyze_business_site(domain: str) -> dict:
    """Fetch the site and extract basic signals about the business."""
    domain = domain.replace("https://", "").replace("http://", "").strip("/")
    url = f"https://{domain}"
    result = {"domain": domain, "ok": False}

    try:
        start = datetime.now()
        with fetch_url(url) as r:
            elapsed = (datetime.now() - start).total_seconds()
            html = r.read().decode("utf-8", errors="ignore")
            result["ok"] = True
            result["load_time"] = round(elapsed, 2)

            # Extract title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
            result["title"] = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else domain

            # Extract meta description
            desc_match = re.search(
                r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']{10,})["\']',
                html, re.IGNORECASE
            )
            result["description"] = desc_match.group(1) if desc_match else None

            # Detect likely AI tool needs
            result["categories"] = detect_categories(html)

            # Basic tech signals
            result["has_blog"] = any(x in html.lower() for x in ['/blog', '/posts', '/articles', 'blog'])
            result["has_newsletter"] = any(x in html.lower() for x in ['newsletter', 'subscribe', 'email list'])
            result["has_shop"] = any(x in html.lower() for x in ['shop', 'store', 'buy now', 'add to cart', 'checkout'])
            result["has_social"] = any(x in html.lower() for x in ['instagram', 'tiktok', 'twitter', 'linkedin', 'facebook'])

    except Exception as e:
        result["error"] = str(e)

    return result


def recommend_ai_tools(site: dict) -> list[dict]:
    """Generate AI tool recommendations based on site analysis."""
    recommendations = []
    categories = site.get("categories", [])

    if site.get("has_blog") or "content" in categories:
        recommendations.append({
            "category": "Content & Writing",
            "tools": ["ChatGPT", "Jasper", "Copy.ai", "Koala Writer"],
            "use_case": f"Auto-generate blog posts and SEO content for {site['domain']}",
            "time_saved": "~5 hours/week",
        })

    if site.get("has_social") or "image" in categories:
        recommendations.append({
            "category": "Social Media & Visuals",
            "tools": ["Canva AI", "Adobe Firefly", "Midjourney", "Opus Clip"],
            "use_case": "Create on-brand visuals and repurpose content across platforms",
            "time_saved": "~3 hours/week",
        })

    if site.get("has_newsletter") or "productivity" in categories:
        recommendations.append({
            "category": "Email & Automation",
            "tools": ["Mailchimp AI", "Beehiiv", "ConvertKit", "Zapier AI"],
            "use_case": "Automate newsletter creation and subscriber workflows",
            "time_saved": "~4 hours/week",
        })

    if site.get("has_shop") or "business" in categories:
        recommendations.append({
            "category": "Sales & Marketing",
            "tools": ["HubSpot AI", "Tidio", "Flair.ai", "Klarna AI"],
            "use_case": "Automate customer support and product descriptions",
            "time_saved": "~6 hours/week",
        })

    if "code" in categories:
        recommendations.append({
            "category": "No-Code & Building",
            "tools": ["Cursor", "Bolt.new", "Lovable", "Framer AI"],
            "use_case": "Build new features and landing pages without a developer",
            "time_saved": "~8 hours/week",
        })

    # Always add a general one if list is short
    if len(recommendations) < 2:
        recommendations.append({
            "category": "General Business AI",
            "tools": ["Notion AI", "Perplexity", "Claude", "Otter.ai"],
            "use_case": "Research, planning, meeting notes, and task management",
            "time_saved": "~3 hours/week",
        })

    return recommendations[:3]


def print_report(site: dict, recommendations: list[dict]):
    domain = site["domain"]

    print(f"\n{'='*60}")
    print(f"  🤖 AI Tools Finder for Founders")
    print(f"  Analyzing: {domain}")
    print(f"{'='*60}\n")

    if not site["ok"]:
        print(f"  ⚠️  Could not analyze {domain}: {site.get('error', 'unknown error')}")
        print(f"  Showing general recommendations instead.\n")
    else:
        print(f"  📋 BUSINESS SNAPSHOT")
        print(f"  {'─'*40}")
        if site.get("title"):
            print(f"  Site title:   {site['title'][:55]}")
        print(f"  Load time:    {site['load_time']}s")
        print(f"  Has blog:     {'Yes' if site.get('has_blog') else 'No'}")
        print(f"  Has shop:     {'Yes' if site.get('has_shop') else 'No'}")
        print(f"  Has social:   {'Yes' if site.get('has_social') else 'No'}")
        print(f"  Newsletter:   {'Yes' if site.get('has_newsletter') else 'No'}")

    print(f"\n  🛠️  AI TOOLS RECOMMENDED FOR YOUR BUSINESS")
    print(f"  {'─'*40}")

    total_time = 0
    for i, rec in enumerate(recommendations, 1):
        hours = int(rec["time_saved"].split("~")[1].split(" ")[0])
        total_time += hours
        print(f"\n  {i}. {rec['category']}")
        print(f"     Tools: {', '.join(rec['tools'])}")
        print(f"     Use:   {rec['use_case']}")
        print(f"     Saves: {rec['time_saved']}")

    print(f"\n  {'─'*40}")
    print(f"  ⏱️  Estimated time saved: ~{total_time} hours/week")
    print(f"  💰 At $50/hr value: ~${total_time * 50}/week reclaimed")

    print(f"\n{'='*60}")
    print(f"  📚 Discover the full directory of AI tools:")
    print(f"  → https://aitrend.info")
    print(f"")
    print(f"  👩‍💼 Connect with founders who use these tools daily:")
    print(f"  → https://aimomfounders.com")
    print(f"{'='*60}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python ai_tool_finder.py <your-business-domain>")
        print("Example: python ai_tool_finder.py mybakery.com")
        sys.exit(1)

    domain = sys.argv[1]

    print(f"\n⏳ Analyzing your business website...")
    site = analyze_business_site(domain)

    recommendations = recommend_ai_tools(site)
    print_report(site, recommendations)


if __name__ == "__main__":
    main()
