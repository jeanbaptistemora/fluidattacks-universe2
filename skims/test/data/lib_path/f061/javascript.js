try {
  try {
    Promise.resolve(x).then(alert('success')).catch();
  } catch {}
} catch (e) {}
