# U-DM 2026 U-16 what-if

An interactive page for the U-16 group of the Danish youth championship (U-DM 2026). It starts from the results of rounds 1–3.

Set results for rounds 4 and 5, and the page simulates the remaining games. It shows each player's chance of finishing first and in the top two. Tiebreaks are Buchholz Cut-1, then Buchholz.

- Game odds come from DSU ratings, with a small advantage for White.
- Round 5 pairings are estimated with a simplified Swiss pairing. The official pairings may differ.
- Source data: [turnering.skak.dk](https://turnering.skak.dk/TournamentActive/Details?tourId=30508&groupId=15432&curtab=tour-table)

## Actual results

Browsers can't read turnering.skak.dk directly, so the **Fetch results** GitHub Action copies the pairings and results into `results.json` about every 10 minutes. You can also start it by hand from the Actions tab. The page's **Fetch actual results** button loads that file. Played games are locked, and official round 5 pairings replace the estimate once they are published.

To refresh the copy yourself, run `python scripts/fetch_results.py results.json`.

View the page through GitHub Pages. If you open `index.html` straight from disk, the fetch button can't load `results.json`.

The page was built with AI assistance (Claude Code).
