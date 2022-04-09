<template>
  <div class="bg">
    <div class="left">
      <p class="name">{{this.name}}</p><br><br>
      <p> Frequent Words: </p>
      <p> {{this.loading}} </p>
      <vue-word-cloud
      style="height: 30vh; width: 30vw"
      :words="ws"
    > </vue-word-cloud>
      <button class = "submit" v-on:click="navigate()">Try other restaurants!</button>
    </div>
    <div class="right">
      <div v-if="this.chartdata.length !== 0" class="chartbg">
        <Chart :styles="chart" :data="chartdata"></Chart>
      </div>
      <div class="filter">
        <div class="filtertitle"> Choose topic: </div>
        <select id = "topic" v-model = "topic" class="dropdown">
          <option value = "Food and Beverage" > Food and Beverage </option>
          <option value = "Place"> Place </option>
          <option value = "Price"> Price </option>
          <option value = "Service"> Service </option>
        </select>
      </div>
      <div class="top">
        <div class="positive" v-if="topic !== ''">
          <p> Top 3 Most Positive Sentences: </p>
          <ul>
            <li v-for="(item,index) in this.sentences[this.topic][0]" :key="index" class="lipos">
              {{ item }}
            </li>
          </ul>
        </div>
        <div class="negative" v-if="topic !== ''">
          <p> Top 3 Most Negative Sentences: </p>
          <ul>
            <li v-for="(item,index) in this.sentences[this.topic][1]" :key="index" class="lineg">
              {{ item }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import VueWordCloud from 'vuewordcloud';
import Chart from './SentimentChart';

export default {
  name: 'Sentiment',
  props: ['name'],
  components: {
    [VueWordCloud.name]: VueWordCloud,
    Chart,
  },
  data() {
    return {
      result: [],
      topic: '',
      ws: [],
      loading: 'Loading...',
      chartdata: [0, 0, 0, 0, 0, 0, 0, 0],
      sentences: {},
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/scrape';
      axios.post(path, { name: this.name })
        .then((res) => {
          this.result = res.data;
          this.sentences = this.result.sentence;
          const resultPos = this.result.result[1];
          const resultNeg = this.result.result[0];
          const r = this.result.wordcount.map((e) => {
            let stdRot = 0;
            if (e[1] > 20) {
              stdRot = 0;
            } else {
              stdRot = this.std_rotations();
            }
            const col = this.random_color();
            return {
              text: e[0],
              weight: e[1],
              rotation: stdRot,
              rotationUnit: 'deg',
              fontFamily: 'Roboto',
              fontStyle: '',
              fontVariant: '',
              fontWeight: e[1],
              color: col,
            };
          });
          this.ws = r;
          this.loading = '';
          this.chartdata = [
            resultPos['Food and Beverage'],
            resultPos.Place,
            resultPos.Price,
            resultPos.Service,
            resultNeg['Food and Beverage'],
            resultNeg.Place,
            resultNeg.Price,
            resultNeg.Service,
          ];
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    navigate() {
      this.$router.push({
        name: 'Input',
      });
    },
    random_color() {
      const colorPalette = [
        '#8ecae6',
        '#219ebc',
        '#023047',
        '#ffb703',
        '#fb8500',
      ];
      return colorPalette[Math.floor(Math.random() * colorPalette.length)];
    },
    std_rotations() {
      const rotations = [0, 0, 90, -90];
      const r = rotations[Math.floor(Math.random() * rotations.length)];
      return r;
    },
  },
  mounted() {
    this.getMessage();
  },
};
</script>

<style scoped>
    @import url('https://fonts.googleapis.com/css?family=Inter');
    .bg {
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    .name {
        font-family: Inter;
        font-style: normal;
        font-weight: bold;
        font-size: 54px;
        line-height: 58px;
        text-align: center;
        margin: 3vh;
        margin-top: 7vh;
        color: #1F335C;
    }
    .left {
      float: left;
      margin-left: 2vw;
      width: 30vw;
    }
    .right {
      margin-left: 37vw;
      width: 55vw;
      margin-top: 5vh;
      border-radius: 8px;
      height: 60vh;
    }
    .submit {
        background: #FCA311;
        border-radius: 8px;
        border-color: #FCA311;
        font-family: Inter;
        font-style: normal;
        font-weight: bold;
        font-size: 24px;
        line-height: 5vh;
        text-align: center;
        width: 25vw;
        height: 12vh;
        margin: 5vh;
        cursor: pointer;
        transition-duration: 0.4s;
        margin-top: 8vh;
    }
    .chart {
      height: 20vh;
      position: relative;
    }
    .chartbg {
      background: #e5e5e5;
      border-radius: 8px;
      padding: 1vh;
    }
    .positive {
      margin-left: 5vw;
    }
    .negative {
      margin-left: 5vw;
    }
    ul {
      display: flex;
      flex-wrap: wrap;
      list-style-type: none;
      padding: 0;
      justify-content: center;
    }
    .lipos {
      display:flex;
      flex-direction:column;
      justify-content:center;
      text-align: center;
      padding: 3vh;
      margin: 2vh;
      border-radius: 10px;
      background-color: #1F335C;
      color: white;
      line-height: 0.5vh;
      width: 10vw;
      margin-top: 0vh;
    }
    .lineg {
      display:flex;
      flex-direction:column;
      justify-content:center;
      text-align: center;
      padding: 3vh;
      margin: 2vh;
      border-radius: 10px;
      background-color: #FCA311;
      line-height: 0.5vh;
      width: 10vw;
      margin-top: 0vh;
    }
    .dropdown {
      font-family: Inter;
      width: 20vw;
      height: 4vh;
      border-radius: 5px;
      margin-top: 2.5vh;
    }
    .filter {
      display:flex;
      justify-content:center;
      text-align: center;
    }
    .filtertitle {
      display:flex;
      flex-direction:column;
      margin-top: 3vh;
      margin-right: 2vh;
    }
    .top {
      display:flex;
    }
</style>
