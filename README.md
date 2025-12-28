# receipt-to-spreadsheet (for my dad)

my dad runs a small rental property business as a side hustle, and tax season always turns into a pile of receipts + a spreadsheet + way too much manual typing.

so, i built a little pipeline that lets him snap a photo of a receipt and get a clean, categorized row added to a spreadsheet (with the image saved for ref).

## what it does
- take a receipt image (jpg/png)
- run ocr to pull raw text
- extract structured fields (vendor, date, total, etc.)
- lets the user quickly review + fix if necessary 
- after approval, appends a new row to a spreadsheet (csv/xlsx) and stores the receipt image

## why it’s unique
this is built around how small rental owners actually track expenses:
- property dropdown
- schedule-e categories
- image attached for audits
- a “confirm” step so you can trust what gets logged

## demo flow
1) upload a receipt photo  
2) extracted fields are shown
3) pick property + category  
4) hit confirm → row gets appended  

## data model (mvp)
```json
{
  "receipt_id": "rcpt_2025_00123",
  "vendor": "home depot",
  "date": "2025-12-18",
  "total": 183.47,
  "tax": 12.34,
  "category": "repairs_and_maintenance",
  "property": "unit_3a",
  "image_url": "uploads/rcpt_2025_00123.jpg",
  "created_at": "2025-12-23T12:40:00Z",
  "confidence": { "vendor": 0.92, "date": 0.88, "total": 0.95 }
}
