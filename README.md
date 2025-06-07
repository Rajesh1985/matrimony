# Vanniyar Manamalai Matrimony

A full-stack matrimony website built with Angular 19.

## Prerequisites

Before you begin, ensure you have the following installed on your Windows computer:

1. **Node.js** (v18.x or later)
   - Download and install from [Node.js official website](https://nodejs.org/)
   - Verify installation: `node --version` and `npm --version`

2. **Git**
   - Download and install from [Git official website](https://git-scm.com/downloads)
   - Verify installation: `git --version`

3. **Angular CLI**
   - Install globally using npm: `npm install -g @angular/cli`
   - Verify installation: `ng version`

## Getting Started

### Clone the Repository

```powershell
git clone https://github.com/Rajesh1985/matrimony.git
cd matrimony/vanniyar-manamalai-app
```

### Install Dependencies

```powershell
npm install
```

### Run the Application

1. **Development server**
   ```powershell
   npm start
   ```
   Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

2. **SSR (Server-Side Rendering) mode**
   ```powershell
   npm run build
   npm run serve:ssr:vanniyar-manamalai-app
   ```
   The SSR version will be available at `http://localhost:4000/`

## Build

- **Production build**
  ```powershell
  npm run build
  ```
  The build artifacts will be stored in the `dist/` directory.

## Running Tests

```powershell
npm test
```

## Troubleshooting Guide

### Common Issues and Solutions

1. **Port 4200 already in use**
   - Close any other running instances of the application
   - Or use: `ng serve --port [different-port-number]`

2. **Node modules issues**
   - Delete node_modules folder and package-lock.json
   - Run `npm cache clean --force`
   - Run `npm install`

3. **Angular CLI version mismatch**
   - Update global Angular CLI: `npm install -g @angular/cli@latest`
   - Update local project: `npm install @angular/cli@latest`

4. **Bootstrap styling issues**
   - Ensure bootstrap is properly imported in angular.json or styles.scss
   - Clear browser cache and reload

5. **TypeScript compilation errors**
   - Run `npm install typescript@latest`
   - Check tsconfig.json for proper configuration
   - Clear TypeScript cache: `rm -rf dist`

### Still Having Issues?

1. Check the console in your browser's developer tools for specific error messages
2. Verify that all prerequisites are installed and up to date
3. Ensure your Node.js version is compatible with the Angular version
4. Try running `npm audit fix` to resolve dependency issues

## Project Structure

```
vanniyar-manamalai-app/
├── src/                     # Source code
│   ├── app/                # Application components
│   │   ├── layout/        # Layout components (navbar, footer)
│   │   └── pages/         # Page components
│   ├── assets/            # Static assets
│   │   ├── images/       # Image files
│   │   └── videos/       # Video files
│   └── styles.scss        # Global styles
└── package.json           # Project dependencies and scripts
```

## Deployment

### Building for Production

Before deploying, make sure to build your application for production:

```powershell
ng build --configuration production
```

This will create a production-ready build in the `dist/vanniyar-manamalai-app/browser` directory.

### Deployment Options

#### 1. Deploy to Azure Web App

1. Create an Azure Web App service
   ```powershell
   az login
   az group create --name matrimony-rg --location eastus
   az webapp create --resource-group matrimony-rg --name vanniyar-manamalai --runtime "node:18-lts"
   ```

2. Deploy using Azure CLI
   ```powershell
   az webapp deployment source config-zip --resource-group matrimony-rg --name vanniyar-manamalai --src dist/vanniyar-manamalai-app/browser
   ```

#### 2. Deploy to Firebase

1. Install Firebase CLI
   ```powershell
   npm install -g firebase-tools
   ```

2. Login to Firebase
   ```powershell
   firebase login
   ```

3. Initialize Firebase project
   ```powershell
   firebase init hosting
   ```

4. Deploy to Firebase
   ```powershell
   firebase deploy
   ```

#### 3. Deploy to Netlify

1. Install Netlify CLI
   ```powershell
   npm install -g netlify-cli
   ```

2. Login to Netlify
   ```powershell
   netlify login
   ```

3. Deploy to Netlify
   ```powershell
   netlify deploy --prod --dir dist/vanniyar-manamalai-app/browser
   ```

### Server-Side Rendering (SSR) Deployment

For SSR deployment:

1. Build the SSR version
   ```powershell
   npm run build:ssr
   ```

2. For Azure Web App deployment with SSR:
   - Update the web.config file in your dist folder
   - Deploy the entire dist folder
   - Set the startup command to: `node server/main.js`

### Post-Deployment Checklist

1. Verify all environment variables are properly set
2. Check if all API endpoints are correctly configured
3. Test the application thoroughly
   - Check all routes
   - Verify image loading
   - Test form submissions
   - Verify SSR functionality
4. Monitor application performance
   - Check load times
   - Verify caching
   - Monitor error rates

### SSL Configuration

1. For Azure: SSL certificates are managed through Azure Portal
2. For Firebase: SSL is automatically handled
3. For Netlify: SSL is automatically provided through Let's Encrypt

### Troubleshooting Production Issues

1. Check application logs in your deployment platform
2. Monitor server resources (CPU, memory usage)
3. Use Application Insights or similar monitoring tools
4. Set up alerts for critical errors
5. Keep regular backups of your database
