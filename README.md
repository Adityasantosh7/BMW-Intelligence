\# BMW Intelligence — Conversational BI Dashboard



> Turn natural language into interactive data dashboards instantly.



🔗 \*\*Live Demo\*\*: https://bmw-intelligence.vercel.app/



\## What it does

Type any business question in plain English and get interactive charts back in seconds. No SQL knowledge required.



\## Tech Stack

| Layer | Technology |

|-------|-----------|

| Frontend | Next.js 16, React, Recharts |

| Orchestration | n8n (PikaPods) |

| LLM | Groq — LLaMA 3.3 70B |

| Database | SQLite via FastAPI microserver |

| Hosting | Vercel (frontend) + PikaPods (n8n) |



\## Features

\- Natural language → SQL → Interactive charts

\- 8-color chart palette with tooltips and zoom

\- Dark / Light mode toggle

\- AI insight on every chart

\- Follow-up questions with chat history

\- CSV upload — query any dataset instantly

\- Reset to BMW dataset with one click

\- Hallucination handling — clear error for out-of-scope questions



\## Dataset

10,781 BMW vehicle listings across 24 models with 9 columns:

model, year, price, transmission, mileage, fuelType, tax, mpg, engineSize



\## Architecture

```

Browser → Vercel (Next.js) → PikaPods (n8n workflow) → FastAPI DB Server → SQLite

&#x20;                                     ↕

&#x20;                              Groq LLaMA 3.3 70B

```



\## Sample Queries

\- "Show average price by BMW model"

\- "Compare diesel vs petrol MPG"

\- "Price trend from 2015 to 2020"

\- "Show mileage vs price correlation"

\- "Which models offer best value under £20,000?"

