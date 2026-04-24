param(
    [Parameter(Mandatory = $true)]
    [string]$InputDocx,

    [Parameter(Mandatory = $false)]
    [string]$OutputPdf = ""
)

$ErrorActionPreference = "Stop"

function Add-TocAtPlaceholder {
    param(
        [object]$Document
    )

    $find = $Document.Content.Find
    $find.ClearFormatting() | Out-Null
    $find.Text = "[[TOC]]"
    $found = $find.Execute()

    if (-not $found) {
        return $false
    }

    $range = $find.Parent
    $range.Text = ""
    $null = $Document.TablesOfContents.Add(
        $range,
        $true,
        1,
        3,
        $true,
        "",
        $true,
        $true,
        "",
        $true,
        $true,
        $true
    )

    return $true
}

$resolvedDocx = (Resolve-Path $InputDocx).Path
$resolvedPdf = $null

if ($OutputPdf) {
    $pdfParent = Split-Path -Parent $OutputPdf
    if ($pdfParent -and -not (Test-Path $pdfParent)) {
        New-Item -ItemType Directory -Path $pdfParent | Out-Null
    }
    $resolvedPdf = [System.IO.Path]::GetFullPath($OutputPdf)
}

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $doc = $word.Documents.Open($resolvedDocx)

    $tocAdded = Add-TocAtPlaceholder -Document $doc

    foreach ($toc in $doc.TablesOfContents) {
        $toc.Update()
    }

    $doc.Fields.Update() | Out-Null
    $doc.Save()

    if ($resolvedPdf) {
        $doc.ExportAsFixedFormat($resolvedPdf, 17)
    }

    $doc.Close()

    [pscustomobject]@{
        input_docx = $resolvedDocx
        toc_added  = $tocAdded
        output_pdf = $resolvedPdf
    } | ConvertTo-Json -Depth 3
}
finally {
    if ($word) {
        $word.Quit()
    }
}
