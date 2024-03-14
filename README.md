# service-depparse-stanza-en
Stanza Dependency Parser for English Language Molfar Service

Returned data is compatible with [Apache ECharts](https://echarts.apache.org/):
```javascript
const dom = document.getElementById('chart-container');

const myChart = echarts.init(dom, null, {
  renderer: 'canvas',
  useDirtyRect: false
});

const inputText = '(any text from which you need to extract dependencies)';
const graph = await extract_dependencies(inputText); // get response from depparse here

const option = {
  legend: [
    {
      data: graph.categories.map(function (a) {
        return a.name;
      })
    }
  ],
  series: [
    {
      type: 'graph',
      layout: 'force',
      edgeSymbol: ['none', 'arrow'],
      data: graph.nodes,
      links: graph.links,
      categories: graph.categories,
      roam: true,
      label: {
        show: true
      },
      edgeLabel: {
        show: true,
        formatter: '{@value}'
      },
      force: {
        repulsion: 100
      }
    }
  ]
};
myChart.setOption(option);
```
