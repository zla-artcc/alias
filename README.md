# ZLA Alias File

ZLA alias file versions and generation templates.

## Rationale

## Repository contents

```
.
├── alias-airplane-data # Airplane information alias codes
├── alias-isr           # ISR files from FE-Buddy
├── alias-tec-routes    # TEC route information
├── output              # [Optional] default directory for newly-created alias files
├── alias.hbs           # ZLA alias template file
├── cwt.txt             # Consolidated wake turbulence information
├── history.txt         # ZLA alias file changelog
```

## How to generate a new alias file

### Locally

If you need to run [dlrey](https://github.com/zla-artcc/dlrey) locally, you'll need to use Git to clone this repo.

If you're unfamiliar with Git, you may consider downloading [GitHub Desktop](https://desktop.github.com/download/). Then follow these steps.

1. Click the green `Code` button at the top-right of this page.<br /><img src="images/clone.png" height="200" />
1. Under the `Local` tab, click `Open with GitHub Desktop`.<br /><img src="images/desktop.png" height="200" />
1. Follow the in-app prompts. If you're having trouble, please don't hesitate to DM @brianknight10 or @wsabransky for help.

### Automation

TODO(wx): explain GHA workflow(s) when they're created, and show how to run them manually if required.

### Creating a release

## Prior releases

All prior releases of the alias file created using this repository can be found on the [Releases page](https://github.com/ZLA-ARTCC/alias/releases).
