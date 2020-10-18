'use strict';
const MANIFEST = 'flutter-app-manifest';
const TEMP = 'flutter-temp-cache';
const CACHE_NAME = 'flutter-app-cache';
const RESOURCES = {
  "main.dart.js": "732caaf5a30a6fdabfe08d2f232b3431",
"manifest.json": "e02a9cb459033a19425fa473543f71a6",
"index.html": "cc5c3cc62e6d1f28c1476434bc47520b",
"/": "cc5c3cc62e6d1f28c1476434bc47520b",
"assets/FontManifest.json": "72619e980b9800b3fa17cf1a739ac8bd",
"assets/packages/cupertino_icons/assets/CupertinoIcons.ttf": "115e937bb829a890521f72d2e664b632",
"assets/fonts/MaterialIcons-Regular.otf": "1288c9e28052e028aba623321f7826ac",
"assets/assets/ic1.png": "8c5ce1ef9bb0ffd0411dda32e7ca0ecd",
"assets/assets/bg.png": "fad539eeac075fd0a15ebcc27b376a1c",
"assets/assets/nature.mp3": "88da45a81a921d533efcb8684401c67b",
"assets/assets/clean.png": "ce1669347c95be265b01634b4eb75979",
"assets/assets/mask.png": "1e17df5376bfcd52951fae2c08f28bfb",
"assets/assets/d.png": "1f7d443a0a0aa70f3ab5fec5a62868fb",
"assets/assets/g1.gif": "850ccbe073fd63d28b6bbf00712eebf1",
"assets/assets/instrumental.mp3": "8d8a4f0e2aa5381132ec1af36d23780b",
"assets/assets/g3.gif": "62859cb175b7636c18a2c25d5318813d",
"assets/assets/w.png": "4dd9258d4f850183ed0ee0ec99612927",
"assets/assets/fonts/nunito.ttf": "d2e691bc4a2b696929172cb3d22ce8ba",
"assets/assets/fonts/openSans.ttf": "3ed9575dcc488c3e3a5bd66620bdf5a4",
"assets/assets/fonts/lato.ttf": "2d36b1a925432bae7f3c53a340868c6e",
"assets/assets/meditate/walk2.png": "6983741a51c2f8b952aa4cc39fc53c39",
"assets/assets/meditate/mindful.png": "1c693ecdef9e9863e9255a2ff92125a1",
"assets/assets/meditate/transc.jpg": "2d787f8a8271d105111e697985ec02c4",
"assets/assets/meditate/walk.png": "d01b7f8ac3fd2489575a6d2b6f29ee09",
"assets/assets/meditate/body.jpg": "be32453bb68fb8aefe03c9b3842c55e5",
"assets/assets/hands.png": "87c8ecd0c583995294d4a7ba9bed063a",
"assets/assets/g2.gif": "7f14f14c603bf6b6a5ca84d1495a1409",
"assets/assets/med.png": "eb3476cf7b760dd332dffe44397a212f",
"assets/assets/indian.mp3": "e04d997b622d0e857b2d8f244d8bba3b",
"assets/assets/beethoven.mp3": "06d2befe2550f262a2c28d03de0bfacc",
"assets/assets/ex.png": "c163af15052604657905b9b3c6da3603",
"assets/assets/dist.png": "3f99107137e7d1e8c8d61c6f73bf3f63",
"assets/assets/christian.mp3": "74fd29338a2106554f9b26e8e5915fab",
"assets/AssetManifest.json": "7821534034b8f9923117900391f388b5",
"assets/NOTICES": "87873520e8a499337e6a29a1de83188d",
"favicon.png": "805078325ca883d801d532c6eb010685",
"icons/Icon-512.png": "4d74d3eaf663a51e6ff603f4a201ef0b",
"icons/Icon-192.png": "4d74d3eaf663a51e6ff603f4a201ef0b",
"version.json": "efa95d2824824581dc74acf5dabc8d43"
};

// The application shell files that are downloaded before a service worker can
// start.
const CORE = [
  "/",
"main.dart.js",
"index.html",
"assets/NOTICES",
"assets/AssetManifest.json",
"assets/FontManifest.json"];
// During install, the TEMP cache is populated with the application shell files.
self.addEventListener("install", (event) => {
  self.skipWaiting();
  return event.waitUntil(
    caches.open(TEMP).then((cache) => {
      return cache.addAll(
        CORE.map((value) => new Request(value + '?revision=' + RESOURCES[value], {'cache': 'reload'})));
    })
  );
});

// During activate, the cache is populated with the temp files downloaded in
// install. If this service worker is upgrading from one with a saved
// MANIFEST, then use this to retain unchanged resource files.
self.addEventListener("activate", function(event) {
  return event.waitUntil(async function() {
    try {
      var contentCache = await caches.open(CACHE_NAME);
      var tempCache = await caches.open(TEMP);
      var manifestCache = await caches.open(MANIFEST);
      var manifest = await manifestCache.match('manifest');
      // When there is no prior manifest, clear the entire cache.
      if (!manifest) {
        await caches.delete(CACHE_NAME);
        contentCache = await caches.open(CACHE_NAME);
        for (var request of await tempCache.keys()) {
          var response = await tempCache.match(request);
          await contentCache.put(request, response);
        }
        await caches.delete(TEMP);
        // Save the manifest to make future upgrades efficient.
        await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
        return;
      }
      var oldManifest = await manifest.json();
      var origin = self.location.origin;
      for (var request of await contentCache.keys()) {
        var key = request.url.substring(origin.length + 1);
        if (key == "") {
          key = "/";
        }
        // If a resource from the old manifest is not in the new cache, or if
        // the MD5 sum has changed, delete it. Otherwise the resource is left
        // in the cache and can be reused by the new service worker.
        if (!RESOURCES[key] || RESOURCES[key] != oldManifest[key]) {
          await contentCache.delete(request);
        }
      }
      // Populate the cache with the app shell TEMP files, potentially overwriting
      // cache files preserved above.
      for (var request of await tempCache.keys()) {
        var response = await tempCache.match(request);
        await contentCache.put(request, response);
      }
      await caches.delete(TEMP);
      // Save the manifest to make future upgrades efficient.
      await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
      return;
    } catch (err) {
      // On an unhandled exception the state of the cache cannot be guaranteed.
      console.error('Failed to upgrade service worker: ' + err);
      await caches.delete(CACHE_NAME);
      await caches.delete(TEMP);
      await caches.delete(MANIFEST);
    }
  }());
});

// The fetch handler redirects requests for RESOURCE files to the service
// worker cache.
self.addEventListener("fetch", (event) => {
  if (event.request.method !== 'GET') {
    return;
  }
  var origin = self.location.origin;
  var key = event.request.url.substring(origin.length + 1);
  // Redirect URLs to the index.html
  if (key.indexOf('?v=') != -1) {
    key = key.split('?v=')[0];
  }
  if (event.request.url == origin || event.request.url.startsWith(origin + '/#') || key == '') {
    key = '/';
  }
  // If the URL is not the RESOURCE list then return to signal that the
  // browser should take over.
  if (!RESOURCES[key]) {
    return;
  }
  // If the URL is the index.html, perform an online-first request.
  if (key == '/') {
    return onlineFirst(event);
  }
  event.respondWith(caches.open(CACHE_NAME)
    .then((cache) =>  {
      return cache.match(event.request).then((response) => {
        // Either respond with the cached resource, or perform a fetch and
        // lazily populate the cache.
        return response || fetch(event.request).then((response) => {
          cache.put(event.request, response.clone());
          return response;
        });
      })
    })
  );
});

self.addEventListener('message', (event) => {
  // SkipWaiting can be used to immediately activate a waiting service worker.
  // This will also require a page refresh triggered by the main worker.
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
    return;
  }
  if (event.data === 'downloadOffline') {
    downloadOffline();
    return;
  }
});

// Download offline will check the RESOURCES for all files not in the cache
// and populate them.
async function downloadOffline() {
  var resources = [];
  var contentCache = await caches.open(CACHE_NAME);
  var currentContent = {};
  for (var request of await contentCache.keys()) {
    var key = request.url.substring(origin.length + 1);
    if (key == "") {
      key = "/";
    }
    currentContent[key] = true;
  }
  for (var resourceKey in Object.keys(RESOURCES)) {
    if (!currentContent[resourceKey]) {
      resources.push(resourceKey);
    }
  }
  return contentCache.addAll(resources);
}

// Attempt to download the resource online before falling back to
// the offline cache.
function onlineFirst(event) {
  return event.respondWith(
    fetch(event.request).then((response) => {
      return caches.open(CACHE_NAME).then((cache) => {
        cache.put(event.request, response.clone());
        return response;
      });
    }).catch((error) => {
      return caches.open(CACHE_NAME).then((cache) => {
        return cache.match(event.request).then((response) => {
          if (response != null) {
            return response;
          }
          throw error;
        });
      });
    })
  );
}
