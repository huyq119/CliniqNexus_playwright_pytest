// Playwright配置文件
const { defineConfig, devices } = require('@playwright/test');

/**
 * @see https://playwright.dev/docs/test-configuration
 */
module.exports = defineConfig({
  testDir: './tests',
  
  // 全局测试超时
  timeout: 30 * 1000,
  
  // 每个测试的超时时间
  expect: {
    timeout: 5000
  },
  
  // 失败时重试次数
  retries: process.env.CI ? 2 : 0,
  
  // 并行工作进程数
  workers: process.env.CI ? 1 : undefined,
  
  // 报告器配置
  reporter: [
    ['html', { outputFolder: 'reports/playwright-report' }],
    ['json', { outputFile: 'reports/playwright-results.json' }],
    ['junit', { outputFile: 'reports/playwright-results.xml' }]
  ],
  
  // 全局设置
  use: {
    // 基础URL
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    
    // 浏览器上下文选项
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    
    // 视口大小
    viewport: { width: 1920, height: 1080 },
    
    // 忽略HTTPS错误
    ignoreHTTPSErrors: true,
    
    // 用户代理
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
  },

  // 项目配置 - 多浏览器测试
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  // 本地开发服务器配置
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
