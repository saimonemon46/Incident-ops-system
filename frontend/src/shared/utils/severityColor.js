export function severityColor(severity) {
  return {
    LOW: 'green',
    MEDIUM: 'amber',
    HIGH: 'orange',
    CRITICAL: 'red',
  }[severity || 'LOW'];
}
