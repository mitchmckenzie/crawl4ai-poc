import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator


async def main():
    # Step 1: Create a pruning filter
    prune_filter = PruningContentFilter(
        # Lower → more content retained, higher → more content pruned
        threshold=0.60,
        # "fixed" or "dynamic"
        threshold_type="dynamic",
        # Ignore nodes with <5 words
        min_word_threshold=5,
    )

    # Step 2: Insert it into a Markdown Generator
    md_generator = DefaultMarkdownGenerator(
        content_filter=prune_filter,
        content_source="raw_html",
        options={
            "skip_internal_links": True,
            "ignore_links": True,
            "ignore_images": True,
            "body_width": 80,
            "include_sup_sub": True,
        },
    )

    # Configure a 2-level deep crawl
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=5, include_external=False, max_pages=50
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True,
        markdown_generator=md_generator,
        exclude_all_images=True,
        exclude_external_links=True,
        exclude_social_media_domains=True,
    )
    scrape_url = "https://omahakidsdentist.com/"
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun(scrape_url, config=config)

        print(f"Crawled {len(results)} pages in total")
        # open file for writing
        with open("crawl_results.md", "w", encoding="utf-8") as f:
            # Access individual results
            for result in results:  # Show first 3 results
                if not result.markdown:
                    continue
                print(f"URL: {result.url}")
                print(result.markdown.fit_markdown)
                print("-" * 1000)
                # write to file
                f.write(result.markdown.fit_markdown)
                f.write(f"URL: {result.url}\n")
                f.write("\n" + "-" * 1000 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
