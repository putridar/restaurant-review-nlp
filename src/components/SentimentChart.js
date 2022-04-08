import { Bar } from 'vue-chartjs';

export default {
  extends: Bar,
  props: ['data', 'options'],
  mounted() {
    this.renderLineChart();
  },
  computed: {
    chartData() {
      return this.data;
    },
  },
  methods: {
    renderLineChart() {
      this.renderChart(
        {
          labels: [
            'Food and Beverage',
            'Place',
            'Price',
            'Service',
          ],
          datasets: [
            {
              label: 'Positive',
              backgroundColor: '#1F335C',
              data: this.chartData.slice(0, 4),
            },
            {
              label: 'Negative',
              backgroundColor: '#FCA311',
              data: this.chartData.slice(4),
            },
          ],
        },
        { responsive: true, maintainAspectRatio: false },
      );
    },
  },
  watch: {
    data() {
      // this._chart.destroy();
      // this.renderChart(this.data, this.options);
      this.renderLineChart();
    },
  },
};
