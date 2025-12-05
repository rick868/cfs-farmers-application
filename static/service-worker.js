const CACHE_NAME = 'agri-platform-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/static/css/styles.css',
    '/static/js/chatbot.js',
    // Add other static assets here
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(ASSETS_TO_CACHE))
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => response || fetch(event.request))
    );
});
