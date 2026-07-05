const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, AlignmentType, ImageRun, LevelFormat,
} = require("docx");

const ACCENT = "1F4E79";
const LIGHT = "EAF1F8";

function h1(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 300, after: 150 } });
}
function h2(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 250, after: 120 } });
}
function body(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 120 },
    children: [new TextRun({ text, size: 22, ...opts })],
  });
}
function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 80 },
    children: [new TextRun({ text, size: 22 })],
  });
}
function statCell(label, value) {
  return new TableCell({
    width: { size: 25, type: WidthType.PERCENTAGE },
    shading: { type: ShadingType.CLEAR, fill: LIGHT },
    margins: { top: 150, bottom: 150, left: 100, right: 100 },
    children: [
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: value, bold: true, size: 30, color: ACCENT })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: label, size: 18 })] }),
    ],
  });
}

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 360, hanging: 260 } } } }],
    }],
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 900, bottom: 900, left: 1000, right: 1000 } } },
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 60 },
        children: [new TextRun({ text: "AI JOB MARKET ANALYSIS", bold: true, size: 44, color: ACCENT })],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 300 },
        children: [new TextRun({ text: "Executive Summary  ·  Data Analyst Project  ·  Obaid Awan", size: 22, italics: true, color: "555555" })],
      }),

      new Paragraph({
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: ACCENT, space: 4 } },
        spacing: { after: 200 },
        children: [new TextRun({ text: "" })],
      }),

      h2("Overview"),
      body("This report summarizes an end-to-end analysis of 2,000 AI-related job postings from 2025, covering salaries, in-demand skills, remote-work patterns, and regional hiring trends. The goal was to answer practical questions a job seeker, hiring manager, or workforce-planning analyst would ask about the AI job market today."),

      h2("Dataset At A Glance"),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [2340, 2340, 2340, 2340],
        rows: [new TableRow({
          children: [
            statCell("Job Postings Analyzed", "2,000"),
            statCell("Job Titles Covered", "15"),
            statCell("Countries", "14"),
            statCell("AI Skills Tracked", "22"),
          ],
        })],
      }),
      new Paragraph({ text: "", spacing: { after: 200 } }),

      h2("Key Findings"),
      bullet("Specialization pays: Applied Scientist ($141.8K avg) and AI Research Engineer ($127.6K avg) roles pay 40-60% more than generalist AI Data Analyst roles ($57.1K avg)."),
      bullet("Experience compounds fast: average salary rises from $63K (Entry) to $98K (Mid) to $138K (Senior) to $187K (Lead)."),
      bullet("Python and SQL are the two most frequently required skills across nearly every AI-adjacent role, regardless of seniority or specialization."),
      bullet("Europe and North America lead in hiring volume (746 and 498 postings respectively), while South Asia shows a fast-growing share, often via remote-friendly roles."),
      bullet("Remote postings draw ~70% more applicants on average than on-site roles (48.4 vs. 28.5) - remote pays slightly more, but is meaningfully more competitive."),
      bullet("AI hiring volume is fairly steady across 2025, with only a mild seasonal dip in December."),

      h2("Recommendations"),
      bullet("Early-career candidates should anchor on Python + SQL fluency before specializing into deep learning frameworks (TensorFlow/PyTorch) or LLM tooling."),
      bullet("Consider hybrid or on-site roles as a lower-competition entry point, then transition to remote roles once a track record is established."),
      bullet("Target Fintech, E-commerce, and Media & Entertainment industries, which show the strongest combination of hiring volume and competitive pay."),
      bullet("For those open to relocation or remote work, North America and Europe currently offer the highest average compensation for AI roles."),

      h2("Methodology"),
      body("Data was processed and analyzed using Python (pandas, matplotlib, seaborn) and SQL (SQLite). The full analysis pipeline - data generation, cleaning, SQL querying, exploratory data analysis, and visualization - is available in the accompanying GitHub-ready project repository, including a fully executed Jupyter notebook and six supporting charts."),

      new Paragraph({
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC", space: 8 } },
        spacing: { before: 300 },
        children: [new TextRun({ text: "Prepared as part of a self-directed Data Analyst portfolio project.", size: 18, italics: true, color: "777777" })],
      }),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("reports/Executive_Summary.docx", buf);
  console.log("Saved reports/Executive_Summary.docx");
});
