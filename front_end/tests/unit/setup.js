global.ResizeObserver = class ResizeObserver {
    observe() {}
    unobserve() {}
    disconnect() {}
};

if (typeof window !== 'undefined') {
    window.matchMedia = window.matchMedia || function matchMedia() {
        return {
            matches: false,
            addListener: () => {},
            removeListener: () => {},
            addEventListener: () => {},
            removeEventListener: () => {},
        };
    };

    window.visualViewport = window.visualViewport || {
        width: 0,
        height: 0,
        addEventListener: () => {},
        removeEventListener: () => {},
    };
}
