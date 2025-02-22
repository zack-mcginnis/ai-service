FROM node:18-slim

WORKDIR /app

# Create package.json with required configuration
RUN echo '{ \
  "name": "reference-app", \
  "version": "0.1.0", \
  "private": true, \
  "dependencies": { \
    "@testing-library/jest-dom": "^5.17.0", \
    "@testing-library/react": "^13.4.0", \
    "@testing-library/user-event": "^13.5.0", \
    "@types/jest": "^27.5.2", \
    "@types/node": "^16.18.0", \
    "@types/react": "^18.2.0", \
    "@types/react-dom": "^18.2.0", \
    "react": "^18.2.0", \
    "react-dom": "^18.2.0", \
    "react-scripts": "5.0.1", \
    "typescript": "^4.9.5", \
    "web-vitals": "^2.1.4" \
  }, \
  "scripts": { \
    "start": "WATCHPACK_POLLING=true react-scripts start", \
    "build": "react-scripts build", \
    "test": "react-scripts test", \
    "eject": "react-scripts eject" \
  }, \
  "eslintConfig": { \
    "extends": [ \
      "react-app", \
      "react-app/jest" \
    ] \
  }, \
  "browserslist": { \
    "production": [ \
      ">0.2%", \
      "not dead", \
      "not op_mini all" \
    ], \
    "development": [ \
      "last 1 chrome version", \
      "last 1 firefox version", \
      "last 1 safari version" \
    ] \
  } \
}' > package.json

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Set environment for React development
ENV NODE_ENV=development
ENV CHOKIDAR_USEPOLLING=true
ENV WATCHPACK_POLLING=true

EXPOSE 3000

CMD ["npm", "start"] 