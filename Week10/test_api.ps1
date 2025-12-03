# Script test tu dong cho Week 10 - Security & Monitoring
# Chay: .\test_api.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Week 10: Security & Monitoring Test  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:3000"

# Kiem tra server co chay khong
Write-Host "Checking if server is running..." -ForegroundColor Yellow
try {
    $null = Invoke-WebRequest -Uri "$baseUrl/hello" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "Server is running!" -ForegroundColor Green
} catch {
    Write-Host "Server is NOT running!" -ForegroundColor Red
    Write-Host "Please start server first: uvicorn main:app --reload --port 3000" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "=== Test 1: Rate Limiting ===" -ForegroundColor Cyan
Write-Host "Sending 8 requests to test rate limit..." -ForegroundColor Yellow
Write-Host ""

$successCount = 0
$blockedCount = 0

for ($i=1; $i -le 8; $i++) {
    Write-Host "Request $i : " -NoNewline
    try {
        $response = Invoke-WebRequest -Uri "$baseUrl/hello" -ErrorAction Stop
        Write-Host "SUCCESS (200)" -ForegroundColor Green
        $successCount++
    } catch {
        if ($_.Exception.Response.StatusCode.value__ -eq 429) {
            Write-Host "BLOCKED (429 - Rate Limit Exceeded)" -ForegroundColor Red
            $blockedCount++
        } else {
            Write-Host "ERROR" -ForegroundColor Magenta
        }
    }
    Start-Sleep -Milliseconds 300
}

Write-Host ""
Write-Host "Results: $successCount successful, $blockedCount blocked" -ForegroundColor Yellow

Write-Host ""
Write-Host "=== Test 2: Monitoring Metrics ===" -ForegroundColor Cyan
Write-Host "Fetching metrics from /metrics endpoint..." -ForegroundColor Yellow
Write-Host ""

try {
    $metrics = Invoke-WebRequest -Uri "$baseUrl/metrics" -ErrorAction Stop
    $metricsContent = $metrics.Content
    
    $requestTotal = ($metricsContent | Select-String -Pattern 'http_request_total' -AllMatches).Matches
    
    if ($requestTotal.Count -gt 0) {
        Write-Host "Request Counter Metrics found!" -ForegroundColor Green
    }
    
    Write-Host "Metrics endpoint is working!" -ForegroundColor Green
    
} catch {
    Write-Host "Failed to fetch metrics" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Test 3: Logging ===" -ForegroundColor Cyan
Write-Host "Checking log file (app.log)..." -ForegroundColor Yellow
Write-Host ""

if (Test-Path "app.log") {
    Write-Host "Log file exists!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Last 10 log entries:" -ForegroundColor Yellow
    Get-Content "app.log" -Tail 10 | ForEach-Object {
        Write-Host $_ -ForegroundColor Gray
    }
} else {
    Write-Host "Log file not found!" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "           Test Complete!              " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
