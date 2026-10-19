# About this fork

Personal fork of [Hantick/ticktick-home-assistant](https://github.com/Hantick/ticktick-home-assistant),
installed through HACS from this repository's releases.

- `main` mirrors upstream `main`.
- `personal` (the default branch) is upstream `main` plus a few patches, one commit per fix. Fixes go
  upstream as pull requests too; once one is merged its commit drops out at the next rebase.
- Releases are tagged `vX.Y.Z-mh.N`, where `X.Y.Z` is upstream's manifest version. The tag points to
  a commit on top of `personal` that only sets `manifest.json`'s version, so `personal` itself never
  carries a version bump that would conflict with upstream.
- `.github/workflows/sync-upstream.yml` runs every Monday (and on demand): it rebases `personal` onto
  upstream `main`, runs compile, hassfest and HACS validation, pushes, and cuts the next release when
  the code changed. On a conflict or failure it opens an issue and changes nothing.

`personal` is rewritten by every rebase. In a local clone, update with
`git fetch origin && git reset --hard origin/personal`.
