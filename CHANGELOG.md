# CHANGELOG


## v2.2.0 (2026-07-24)

### Bug Fixes

- Update sha256 hashes in GQLOperations and add platform field in Twitch class
  ([`c8b8f4e`](https://github.com/nthnunes/twitch-miner/commit/c8b8f4eb6f6ee32eeef0f412323d496709469346))

- Updated sha256 hashes for persisted queries in GQLOperations. - Added 'platform' field with value
  'web' in Twitch class for improved context handling. - Enhanced error handling for invalid
  responses in load_channel_points_context method.

### Features

- Enhance ad handling with new normalization and click logic
  ([`898c82d`](https://github.com/nthnunes/twitch-miner/commit/898c82db2c514462b720963344624e69e9193372))

- Added functions to normalize ad slots and pages from API responses. - Introduced click chance
  handling and ad load timeout configurations. - Updated `get_ads_config_from_api` to support new
  data structure. - Improved ad clicking logic with randomized delays and error handling.

- Implement multi-account support
  ([`3c628dc`](https://github.com/nthnunes/twitch-miner/commit/3c628dc1185b73eecb28e46bbd3ac9d4872131af))

- Integrate versioning system and update version references
  ([`c19117b`](https://github.com/nthnunes/twitch-miner/commit/c19117bf81abb26ab4c58d4fadd9e0bbfd8bd010))

- Introduced a new `_version.py` file to manage the application version. - Updated all relevant
  files to reference the version dynamically using `__version__`. - Removed the outdated
  `changelog.md` file. - Added `pyproject.toml` for semantic versioning configuration. - Created
  `requirements-build.txt` for fixed dependencies during the build process. - Implemented a GitHub
  Actions workflow for automated releases.

### Refactoring

- Update uninstaller UI and remove unused dependencies
  ([`ca2a509`](https://github.com/nthnunes/twitch-miner/commit/ca2a5098e2173400fe2241a7cb6fc7a3827f27f7))

- Enhanced the uninstaller interface with a new graphical layout using tkinter. - Removed inquirer
  and other unused dependencies from the project. - Updated the uninstaller logic to improve user
  experience and error handling. - Adjusted the build process in the GitHub Actions workflow to
  reflect these changes.


## v2.1.4 (2026-03-01)

### Chores

- Bump version to 2.1.4
  ([`79c59f2`](https://github.com/nthnunes/twitch-miner/commit/79c59f2899e8d616be28bdeec4b1e08d456cd618))

- Update changelog for version 2.1.4 with improvements in API handling and interface refactoring
  ([`8382ed6`](https://github.com/nthnunes/twitch-miner/commit/8382ed63f5114a453c0a4cfa2978d2cf786951f0))

### Refactoring

- Enhance API response handling and configuration for ad viewing durations
  ([`8186826`](https://github.com/nthnunes/twitch-miner/commit/81868264c93d870ba48fada06b62459d2abe1c36))

- Remove analytics menu and comment out analytics call
  ([`7bee1cc`](https://github.com/nthnunes/twitch-miner/commit/7bee1cc4666ae46906247aa112dfcb804067894c))


## v2.1.3 (2025-11-18)

### Bug Fixes

- Handle StreamerDoesNotExistException when loading channel points context
  ([`ce1e2ef`](https://github.com/nthnunes/twitch-miner/commit/ce1e2efa674f3517894ba2e35d2a85ca6c52b9cd))

- Update sha256Hash values in GQLOperations for improved security
  ([`a2bf3fe`](https://github.com/nthnunes/twitch-miner/commit/a2bf3fe0c07ea53cb847d8d0159a6f675ed8235a))

### Chores

- Bump version to 2.1.3
  ([`4bc470a`](https://github.com/nthnunes/twitch-miner/commit/4bc470a2bbab044a9032ff8fd080e638d0cb3566))

- Update changelog for version 2.1.3 with bug fixes and improvements in streamer selection and
  GraphQL operations
  ([`103a010`](https://github.com/nthnunes/twitch-miner/commit/103a010b3013d9fc5f0b891cacae4b3271ce3809))

### Refactoring

- Limit the number of streamers watched to two and improve priority handling in Twitch class
  ([`d8327a6`](https://github.com/nthnunes/twitch-miner/commit/d8327a69374f269dc912f6d92b30bd4bac0b0656))

- Rename GraphQL operation from UserByLogin to GetIDFromLogin for clarity in channel ID retrieval
  ([`cc5fc71`](https://github.com/nthnunes/twitch-miner/commit/cc5fc719449e4a730a4c9e5d1b1eb27fa842f4cc))


## v2.1.2 (2025-11-11)

### Bug Fixes

- Update GraphQL operations to use UserByLogin for channel ID retrieval and user data
  ([`5765986`](https://github.com/nthnunes/twitch-miner/commit/576598681326c65a9b9dbec5a665d9207cea66db))

### Chores

- Add changelog detailing new features, improvements and bug fixes
  ([`c4461ca`](https://github.com/nthnunes/twitch-miner/commit/c4461ca40b51f90d8ca4afc05f80610d22104aaa))

- Bump version to 2.1.2
  ([`9e2e616`](https://github.com/nthnunes/twitch-miner/commit/9e2e616256f6e619880ba62df46dc31eb4b556d5))

- Update changelog for version 2.1.2 with bug fixes for GraphQL calls and campaign synchronization
  ([`0c5bc6b`](https://github.com/nthnunes/twitch-miner/commit/0c5bc6bb57d7db8c9fff7de5fd6e55a949a933a6))


## v2.1.1 (2025-10-04)


## v2.1.0 (2025-06-05)

### Bug Fixes

- Add error handling for page loading in ads viewer
  ([`6ad0ba3`](https://github.com/nthnunes/twitch-miner/commit/6ad0ba37d206ed73a25d25aa02845ee4ab2ed275))

- Add prefix to log message for better context in Twitch viewer
  ([`97ebe39`](https://github.com/nthnunes/twitch-miner/commit/97ebe39730fe869ffb1c87f6ace5ef0bbaf4026b))

- Bring back create shortcut
  ([`0371cec`](https://github.com/nthnunes/twitch-miner/commit/0371cecb57cc1017efb67f8e24d8bd97cf84b949))

- Bugs adjusts
  ([`232d0a4`](https://github.com/nthnunes/twitch-miner/commit/232d0a4b73b8c48260c07e37d2721201d4fdb8b2))

- Check for updates when starts
  ([`4d57d66`](https://github.com/nthnunes/twitch-miner/commit/4d57d6684a3298caabdb3b9a0d7f787350720555))

- Correct spacing in version log message
  ([`8697042`](https://github.com/nthnunes/twitch-miner/commit/8697042a3124156250ea0273a08342b6765726cf))

- Exit before update
  ([`e6f25ce`](https://github.com/nthnunes/twitch-miner/commit/e6f25ce65d1f5adacf1ccab8f47b37e4a01be2e0))

- Import icons from right path
  ([`dc1cbb4`](https://github.com/nthnunes/twitch-miner/commit/dc1cbb492e079d719892ee45b7f8d5df5ac51fb4))

- Permission bugs
  ([`39dcd4d`](https://github.com/nthnunes/twitch-miner/commit/39dcd4d9657490678a813d81295906f374e67307))

- Solve error fetching PlaybackAccessToken
  ([`2980e8e`](https://github.com/nthnunes/twitch-miner/commit/2980e8e22133c42b3ed0e24ac204dacb5d80b6e7))

- Update path handling for TwitchMiner executable
  ([`3ae805f`](https://github.com/nthnunes/twitch-miner/commit/3ae805fc0d60ae8b3fdc253d068580adccf2a4ca))

### Chores

- Bump version to 2.0.2
  ([`f672b0c`](https://github.com/nthnunes/twitch-miner/commit/f672b0c9d84fe0897f5e9984d7be1c8a516a872d))

- Bump version to 2.0.5
  ([`f540b90`](https://github.com/nthnunes/twitch-miner/commit/f540b90a6311fb5c623fc8806737e62af5a64570))

- Bump version to 2.0.6
  ([`2aa089e`](https://github.com/nthnunes/twitch-miner/commit/2aa089e254abb61806b868ee5e817091f1e36fba))

- Bump version to 2.1.0
  ([`5032085`](https://github.com/nthnunes/twitch-miner/commit/50320855ed0523bfec934052259f6ca422f3a26f))

- Bump version to 2.1.1
  ([`359a1d2`](https://github.com/nthnunes/twitch-miner/commit/359a1d26a0d001d650eecd394b0780b14ddf3822))

- Bump verstion to 2.0.1
  ([`cc0f8c8`](https://github.com/nthnunes/twitch-miner/commit/cc0f8c84d328636205dbeaba22a8a1fc0e99addf))

- Remove Dockerfile as it is no longer needed
  ([`c374d68`](https://github.com/nthnunes/twitch-miner/commit/c374d68844551a67d95ea7f41133bd5ec35e4def))

- Remove unused configuration files and image assets
  ([`7a53b1b`](https://github.com/nthnunes/twitch-miner/commit/7a53b1b63f3ec1a81bac15c28d6ed5ac9b86fdb0))

- Update monitored Twitch channel name from 'boimoraes' to 'nthnunes'
  ([`26708ea`](https://github.com/nthnunes/twitch-miner/commit/26708ea153b1db6d3715b8a7788e6ac69fdd4472))

### Documentation

- Add build instructions for creating a standalone executable using PyInstaller
  ([`4ba660b`](https://github.com/nthnunes/twitch-miner/commit/4ba660bf69146779337c997e932de031fe432b40))

- Update PyInstaller command to include custom icon for executable
  ([`084b2ef`](https://github.com/nthnunes/twitch-miner/commit/084b2ef0483cb1ac9b74518d57bf547f32d7ec19))

### Features

- 1.9.9.1
  ([`2236872`](https://github.com/nthnunes/twitch-miner/commit/2236872daa45c0f8372fdd5f41920376dad5fdf5))

- Add API call to register client with Twitch username and last sign-in timestamp
  ([`a86c5fb`](https://github.com/nthnunes/twitch-miner/commit/a86c5fbf2eb18a4e6177fd43193d8719f09892f2))

- Add auto updater
  ([`c3ed464`](https://github.com/nthnunes/twitch-miner/commit/c3ed46451e3d9a9a87094e71552d827694a05971))

- Add button to view StreamElements store
  ([`982061c`](https://github.com/nthnunes/twitch-miner/commit/982061c3d85103d84ca0557af57e6fca0ad4529d))

- Add chat notifications settings and functionality
  ([`a11f55c`](https://github.com/nthnunes/twitch-miner/commit/a11f55c5c69f178bc92a8b16a0ae001db8eb3aab))

- Add connected chats notifications
  ([`0ad22c6`](https://github.com/nthnunes/twitch-miner/commit/0ad22c6dd69c0f917ed7b03a03cd7a4bf23163ea))

- Add flask
  ([`1d36659`](https://github.com/nthnunes/twitch-miner/commit/1d36659a4c888fafc0c0d5a1b66015cc9fedff0e))

- Add flask
  ([`44cc9b3`](https://github.com/nthnunes/twitch-miner/commit/44cc9b3d5dd60202cb0d114b8534adc58e927a7a))

- Add installer
  ([`7dd150f`](https://github.com/nthnunes/twitch-miner/commit/7dd150ffcbce22fd8e6697d5fcff0bde38d327c9))

- Add settings and about tabs, implement theme loading and saving functionality
  ([`745f490`](https://github.com/nthnunes/twitch-miner/commit/745f490fad950ec1b9a7efa8a519745885530d7e))

- Add support for custom Chromium path and enhance browser automation masking
  ([`c7a82d8`](https://github.com/nthnunes/twitch-miner/commit/c7a82d804a29dcc495bdf154834cf88ff09efd49))

- Add ui for edit streams and username
  ([`3135755`](https://github.com/nthnunes/twitch-miner/commit/31357557bb61982429f0db74b8301956d8a89ba6))

- Add uninstaller
  ([`b8299f6`](https://github.com/nthnunes/twitch-miner/commit/b8299f625b9073c1f61257392c823b869ae7a254))

- Add updater
  ([`2da4a7a`](https://github.com/nthnunes/twitch-miner/commit/2da4a7ae8ffb0b0762c1298a73e275b40f2c99d7))

- Add user data configuration with email validation and save functionality
  ([`4cf15f3`](https://github.com/nthnunes/twitch-miner/commit/4cf15f366c15e54c51db2aa0bfeef57f38ad4f07))

- Add window icon support to main and user configuration windows
  ([`dbce80c`](https://github.com/nthnunes/twitch-miner/commit/dbce80cb52be2e8908341265b82a00f63e999e07))

- Add Windows toast notifications for Twitch chat mentions
  ([`a61b772`](https://github.com/nthnunes/twitch-miner/commit/a61b772ebb2127465048c6e96ad0bf8f163f069d))

- Bump version to 2.0.3
  ([`53ecdee`](https://github.com/nthnunes/twitch-miner/commit/53ecdee62555d3aacc2ae0d351fc5dfc7a3e789a))

- Implement ads viewer functionality
  ([`ea727f4`](https://github.com/nthnunes/twitch-miner/commit/ea727f45c02347989d9e4a9fc5a454e9937d34b3))

- Implement fallback mechanism for username retrieval from config.json and username.txt
  ([`71feae3`](https://github.com/nthnunes/twitch-miner/commit/71feae3fd3bde52d5dc98243dc6397c0571f3a0d))

- Implement main application with GUI
  ([`59cecfe`](https://github.com/nthnunes/twitch-miner/commit/59cecfe2b1bbe9ce98807af98f9f233976d3b177))

- Implement retry mechanism for API URL fetching with exponential backoff
  ([`52fa71c`](https://github.com/nthnunes/twitch-miner/commit/52fa71c19fac3d2e63a9fae5a5a72eaec318a2aa))

- Remake ui with custom tkinter
  ([`29cc833`](https://github.com/nthnunes/twitch-miner/commit/29cc83387ac4feae47898d5eafb986ddc55f0675))

- Update README with new features and installation instructions
  ([`1faf9a4`](https://github.com/nthnunes/twitch-miner/commit/1faf9a43c76904fff7461bb34005bea07b36b9dc))

### Refactoring

- Adjust folders schema
  ([`051d708`](https://github.com/nthnunes/twitch-miner/commit/051d70890e4513c28a5e6b55f41df0387a9dccc7))

- Comment out error and info logging for API URL fetching
  ([`78a88c9`](https://github.com/nthnunes/twitch-miner/commit/78a88c90b5b9fbfab6a1907ba84f389535963589))

- Migrate configuration from .dat to .json format and implement new config management functions
  ([`2488014`](https://github.com/nthnunes/twitch-miner/commit/2488014eb1aeccabb2c6265aea5c0dff57107e5b))

- Replace remote icon fetching with local image asset for system tray
  ([`baf523e`](https://github.com/nthnunes/twitch-miner/commit/baf523e90b198639655d6bbcee4fe9382d419120))

- Update labels
  ([`4fba779`](https://github.com/nthnunes/twitch-miner/commit/4fba7797e4b4973f3cf939fa8418ee6db8a55584))

- Update twitch_viewer to use synchronous Playwright and simplify channel monitoring logic
  ([`98c94ac`](https://github.com/nthnunes/twitch-miner/commit/98c94ac963b3c316af49cdcd611f85ce0a975bca))

- Update user tab to reflect changes from "Planos" to "Addons" and modify associated content
  ([`ab2010c`](https://github.com/nthnunes/twitch-miner/commit/ab2010c8612f0381c48499f9df678a61675616a3))


## v1.9.9 (2024-11-03)

### Features

- 1.9.9
  ([`c9a75aa`](https://github.com/nthnunes/twitch-miner/commit/c9a75aa291af066cff4cbf8075f666a0e690b290))

- Add readme
  ([`f6c5f78`](https://github.com/nthnunes/twitch-miner/commit/f6c5f780e41dadf6361d2bb79180f447d56d4fd2))

- Add run file
  ([`2ffccae`](https://github.com/nthnunes/twitch-miner/commit/2ffccae6283b4ad1e77276caa508ec0c75f91180))

- All project
  ([`3f0d0e7`](https://github.com/nthnunes/twitch-miner/commit/3f0d0e7386f2e0462897b51ff1834f205f9af762))
