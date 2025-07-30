<script>
import { Chart, registerables } from 'chart.js/auto'
import ChartDataLabels from 'chartjs-plugin-datalabels'

Chart.register(...registerables, ChartDataLabels)

export default {
  props: ['endpoint'],
  data() {
    return {
      chart: null,
      chartData: {}
    }
  },
  async mounted() {
    const res = await fetch(this.endpoint, {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem('token')}`
      }
    })

    const data = await res.json()
    this.chartData = data

    const ctx = this.$refs.canvas.getContext('2d')

    const isGrouped = Array.isArray(data.datasets)
    const type = isGrouped ? 'bar' : this.getChartType(data.labels.length)
    const useHorizontal = type === 'bar' && data.labels.length > 10

    const config = {
      type,
      data: {
        labels: data.labels,
        datasets: isGrouped ? data.datasets : [{
          label: data.label,
          data: data.values,
          backgroundColor: data.bgColors || this.defaultColors(data.values.length),
          borderRadius: 8,
          borderWidth: 1,
          hoverOffset: 10
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: type === 'doughnut' ? '60%' : undefined,
        indexAxis: useHorizontal ? 'y' : 'x',
        plugins: {
          legend: {
            display: isGrouped || type === 'doughnut',
            position: 'bottom'
          },
          tooltip: {
            enabled: true
          },
          datalabels: {
            display: !isGrouped && type !== 'doughnut',
            color: '#fff',
            font: {
              weight: 'bold',
              size: 10
            },
            formatter: value => value
          }
        },
        scales: type === 'doughnut' ? {} : {
          x: {
            stacked: isGrouped,
            ticks: {
              color: '#333',
              font: { size: 10 }
            }
          },
          y: {
            stacked: isGrouped,
            beginAtZero: true,
            ticks: {
              color: '#333',
              font: { size: 10 }
            }
          }
        }
      },
      plugins: [ChartDataLabels]
    }

    this.chart = new Chart(ctx, config)
  },
  methods: {
    getChartType(count) {
      return count <= 3 ? 'doughnut' : 'bar'
    },
    defaultColors(length) {
      const palette = [
        '#4B9CD3', '#FF6384', '#36A2EB', '#FFCE56',
        '#8E44AD', '#2ECC71', '#F39C12', '#E74C3C',
        '#1ABC9C', '#95A5A6', '#34495E', '#C0392B'
      ]
      return Array.from({ length }, (_, i) => palette[i % palette.length])
    }
  }
}
</script>

<template>
  <div class="col-12 col-md-6 col-lg-4 mb-4">
    <div class="card h-100 shadow-sm border">
      <div class="card-body">
        <h5 class="card-title text-center text-dark mb-3">
          {{ chartData.title }}
        </h5>
        <div style="max-height: 400px; overflow-y: auto;">
          <canvas ref="canvas" :height="chartData.labels?.length * 22 || 300"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
canvas {
  width: 100% !important;
}
</style>
