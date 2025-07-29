const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {"start":"_app/immutable/entry/start.CXYNbtUa.js","app":"_app/immutable/entry/app.MvE7kCt-.js","imports":["_app/immutable/entry/start.CXYNbtUa.js","_app/immutable/chunks/client.CVMEu4Wy.js","_app/immutable/entry/app.MvE7kCt-.js","_app/immutable/chunks/preload-helper.D6kgxu3v.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-BAFT3txh.js')),
			__memo(() => import('./chunks/1-CKIUjXlG.js')),
			__memo(() => import('./chunks/2-BzTysezS.js').then(function (n) { return n.aE; }))
		],
		routes: [
			{
				id: "/[...catchall]",
				pattern: /^(?:\/(.*))?\/?$/,
				params: [{"name":"catchall","optional":false,"rest":true,"chained":true}],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

const prerendered = new Set([]);

const base = "";

export { base, manifest, prerendered };
//# sourceMappingURL=manifest.js.map
