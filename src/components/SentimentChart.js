import { Bar } from 'vue-chartjs';

export default {
  extends: Bar,
  data: () => ({
    chartdata: {
      labels: ['January', 'February'],
      datasets: [
        {
          label: 'Data 1',
          backgroundColor: '#f87979',
          data: [40, 30],
        },
        {
          label: 'Data 2',
          backgroundColor: '#f87979',
          data: [30, 20],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true,
          },
        }],
      },
    },
  }),

  mounted() {
    this.renderChart(this.chartdata, this.options);
  },
};
