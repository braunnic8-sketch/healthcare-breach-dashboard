[README (1).md](https://github.com/user-attachments/files/34697536/README.1.md)
# HHS Healthcare Breach Dashboard — Shared Student Template

## No Python installation required

1. Prepare your combined HHS current + archived Excel workbook. Use submission dates from January 1, 2020 through December 31, 2025, and preserve the November 10, 2026 snapshot.
2. Save the workbook as **hhs_breaches.xlsx**. The data should be in the **first worksheet**, with column headings in row 1.
3. Create a GitHub account at https://github.com and a new repository.
4. Upload **app.py**, **requirements.txt**, and **hhs_breaches.xlsx** to the root of the repository. Do not upload private patient information.
5. Visit https://share.streamlit.io/ and sign in with GitHub. Select **Create app**, your repository, your branch, and **app.py** as the entry point. Deploy.
6. Open the app URL. Use the sidebar to filter the data; the three charts and summary values will update.
7. Submit your app URL, research question, three findings, and risk management recommendations as directed by your instructor.

## Built-in features
- Year, state, breach type, covered entity type, business associate, and information-location filters when the columns exist
- Adjustable minimum number of individuals affected
- Bar chart, annual trend, histogram, data table, and CSV download

## Notes
- If the workbook has a different name, change `FILENAME` near the top of app.py.
- If column headings differ, use the original HHS field names or adjust the `find_col` aliases in app.py.
- A missing field simply disables the corresponding chart/filter; check your headers if you expected it.
- Current and archived HHS reports are status-based collections. Preserve original files, note the snapshot date, and check overlaps before appending.
- This is a common starting point. The three prebuilt charts may not be the best three for every team's question. Teams must explain relevance and may need to adapt their dashboard with instructor guidance.
- The data cover reported large breaches and cannot establish the probability of a breach at a specific organization. The sum of individuals affected is not necessarily the number of unique individuals.
