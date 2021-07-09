# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2021-07-09
### Added
- Showing total score for task in table #2.
- Today score #5.
- Yesterday score.
- Average score.
- Sorting by score
### Changed
- Sorting tags by score, if grouping is by tags #4.

## [0.3.1] - 2021-07-08
### Fixed
- Sorting by date if some task don't have complition.

## [0.3.0] - 2021-07-08
### Added
- Improve printing of header and rows.
- Class for working with time.
- Show today completed tasks with green color #1.
### Changed
- Move custom exception to exceptions.py.
### Fixed
- Show only headers when database is empty.

## [0.2.0] - 2021-07-07
### Changed
- Move Colors class to colors.py.
- Move load and save json functions to files.py.
### Fixed
- Incorrect type of tags in tasks.py.

## [0.1.0] - 2021-07-06
### Added
- Set up template.
- Adding task with name, tags, difficulty.
- Editing task with name, tags, difficulty.
- Completion task with date of complition.
- Display task as table in console.
- Group tasks by difficulty, tags, count of complition, date of last complition.
- Sort tasks by id, name, difficulty, count of complition, date of last complition.
- Save data to platform specific app data dir.
### Fixed
- README.md
