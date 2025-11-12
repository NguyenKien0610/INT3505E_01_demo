const newman = require('newman');

newman.run({
  collection: require('./Product_API_Tests.postman_collection.json'),
  reporters: ['cli', 'html'],
  reporter: { html: { export: './report.html' } }
}, (err) => {
  if (err) throw err;
  console.log('✅ Test suite completed. Report saved at report.html');
});
