## GitHub Copilot Chat

- Extension Version: 0.22.4 (prod)
- VS Code: vscode/1.95.3
- OS: Mac

## Network

User Settings:
```json
  "github.copilot.advanced": {
    "debug.useElectronFetcher": true,
    "debug.useNodeFetcher": false
  }
```

Connecting to https://api.github.com:
- DNS ipv4 Lookup: 20.27.177.116 (21 ms)
- DNS ipv6 Lookup: ::ffff:20.27.177.116 (1 ms)
- Electron Fetcher (configured): HTTP 200 (65 ms)
- Node Fetcher: HTTP 200 (41 ms)
- Helix Fetcher: HTTP 200 (146 ms)

Connecting to https://api.individual.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 140.82.112.21 (19 ms)
- DNS ipv6 Lookup: ::ffff:140.82.112.21 (1 ms)
- Electron Fetcher (configured): HTTP 200 (838 ms)
- Node Fetcher: HTTP 200 (626 ms)
- Helix Fetcher: HTTP 200 (820 ms)

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).