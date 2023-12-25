# ms-codesigning-roots

This repository contains an automatically updated bundle
of Microsoft's root store for code signing, i.e. certificates
with the `codeSigning` EKU.

The bundle is available in [bundle.pem](./bundle.pem)

## Why?

This repository is virtually identical to the content provided
by the [CCADB]. It serves only two purposes:

1. To munge some additional metadata out of each certificate,
   for easier searching;
2. To act as an (unauthenticated) transparency record for changes to Microsoft's
   root store, using [Simon Willison's "Git scraping" idiom].

[CCADB]: https://www.ccadb.org/resources

[Simon Willison's "Git scraping" idiom]: https://simonwillison.net/2020/Oct/9/git-scraping/
