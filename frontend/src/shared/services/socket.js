export function createSocketClient() {
  return {
    connected: false,
    subscribe: () => () => {},
    publish: () => {},
  };
}
