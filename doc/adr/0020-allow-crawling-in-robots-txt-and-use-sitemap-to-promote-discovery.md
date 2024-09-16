# 20. Allow crawling in robots.txt and use sitemap to promote discovery

Date: 2024-09-16

## Status

Accepted

## Context

At the moment our `robots.txt` explicitly disallows crawling of the site. This is nominally to discourage search engines from indexing judgments, however search engines may still index pages where they are linked to from other sites, using related terms on those pages to infer the title or content of the document.

For each document on the service we do provide a `noindex` robots directive both through HTML meta tags and HTTP headers, but because crawling and scraping of the page is forbidden by `robots.txt` search engines will not crawl the page in order to discover that they shouldn't index it. This means that pages may appear in search engines.

The spirit of the service is that individual documents should not appear in search indexes, and to achieve this we (somewhat counter-intuitively) need to allow crawling so that search engines can discover that they shouldn't include pages in their index.

## Decision

- `robots.txt` on Public UI will be changed to allow crawling of the entire site
- A new sitemap, rooted in `sitemap.xml`, will be provided which allows easy discovery of all documents for the purposes of crawling. This means search engines can rapidly discover the entire corpus of documents, crawl them, and mark them for exclusion from their search indexes.
- This sitemap will be included in `robots.txt`, as well as manually submitted to major search engines.

## Consequences

- Search engines which obey robot `noindex` directives will be better able to proactively flag documents as not for inclusion in the index.
- Users looking to crawl the site will be able to discover all site content.
