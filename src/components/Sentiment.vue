<template>
  <div class="bg">
    <div class="title">
      <button class = "submit2" v-on:click="getMessage()">Refresh</button>
      <p class="name">{{this.name}}</p><br><br>
      <button class = "submit" v-on:click="navigate()">Try other restaurants!</button>
    </div>
    <div class="top">
      <div>
      <div class="col1">
        <div class="col">
          <div class="num"> {{this.total}} </div><br>
          <div class="txt"> Reviews </div>
        </div>
          <div class="col">
          <div class="num">{{this.positive}}% </div><br>
          <div class="txt"> Positive reviews </div>
        </div>
      </div>
      <p> Frequent Words: </p>
        <p> {{this.loading}} </p>
        <vue-word-cloud
        style="height: 30vh; width: 40vw"
        :words="ws"
      > </vue-word-cloud>
      </div>
      <div class="col">
        <div v-if="this.chartdata.length !== 0" class="chartbg">
          <Chart :styles="chart" :data="chartdata"></Chart>
        </div>
      </div>
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
    <div class="bottom">
      <div>
        <div class="positive" v-if="topic !== ''">
          <p> Top 3 Most Positive Reviews: </p>
          <ul>
            <li v-for="(item,index) in this.sentences[this.topic][1]" :key="index" class="lipos">
              {{ item }}
            </li>
          </ul>
        </div>
        <div class="negative" v-if="topic !== ''">
          <p> Top 3 Most Negative Reviews: </p>
          <ul>
            <li v-for="(item,index) in this.sentences[this.topic][0]" :key="index" class="lineg">
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
      total: 0,
      positive: 0,
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/scrape';
      axios.post(path, { name: this.name })
        .then((res) => {
          this.result = res.data;
          this.get_top_3(this.result.sentence);
          this.total = this.result.total;
          this.positive = Math.round(this.result.positive) / 100;
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
    get_top_3(x) {
      const top3 = {
        'Food and Beverage': [],
        Place: [],
        Price: [],
        Service: [],
      };
      for (const [key, value] of Object.entries(x)) {
        for (let [sentiment, val] of Object.entries(value)) {
          val = val.sort((a, b) => b.Score - a.Score);
          const chosen = val.slice(0, 3);
          const sentence = [];
          for (const id in chosen) {
            sentence.push(chosen[id].Sentence);
          }
          top3[key].push(sentence);
        }
      }
      this.sentences = top3;
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
        font-size: 60px;
        line-height: 58px;
        text-align: center;
        margin: 3vh;
        color: #1F335C;
        margin-bottom: 0vh;
        margin-right: 8vw;
        margin-left: 12vw;
    }
    .title {
      display: flex;
      justify-content:center;
      text-align: center;
    }
    .left {
      float: left;
      margin-left: 2vw;
      width: 30vw;
    }
    .right {
      margin-left: 37vw;
      width: 55vw;
      margin-top: 0vh;
      border-radius: 8px;
      height: 60vh;
    }
    .bottom {
      display: flex;
      justify-content:center;
      text-align: center;
    }
    .submit {
      background: #FCA311;
      border-radius: 8px;
      border-color: #FCA311;
      font-family: Inter;
      font-style: normal;
      font-weight: bold;
      font-size: 22px;
      line-height: 4vh;
      text-align: center;
      width: 20vw;
      height: 10vh;
      margin: 5vh;
      cursor: pointer;
      transition-duration: 0.4s;
      margin-top: 2.5vh;
    }
    .submit2 {
      background: #FCA311;
      border-radius: 8px;
      border-color: #FCA311;
      font-family: Inter;
      font-style: normal;
      font-weight: bold;
      font-size: 22px;
      line-height: 4vh;
      text-align: center;
      width: 15vw;
      height: 10vh;
      margin: 5vh;
      margin-left: 8vh;
      cursor: pointer;
      transition-duration: 0.4s;
      margin-top: 2.5vh;
    }
    .chart {
      height: 20vh;
      position: relative;
      width: 35vw;
    }
    .chartbg {
      background: #e5e5e5;
      border-radius: 8px;
      padding: 1vh;
      width: 35vw;
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
      width: 60vw;
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
      width: 60vw;
      margin-top: 0vh;
    }
    .dropdown {
      font-family: Inter;
      width: 20vw;
      height: 4vh;
      border-radius: 5px;
    }
    .filter {
      display:flex;
      justify-content:center;
      text-align: center;
    }
    .filtertitle {
      display:flex;
      flex-direction:column;
      margin-right: 2vh;
    }
    .top {
      display:flex;
      justify-content:center;
      text-align: center;
    }
    .col1 {
      display:flex;
      justify-content:center;
      text-align: center;
    }
    .col {
      margin: 3vw;
      margin-top: 2vh;
    }
    .num {
      font-size: 9vh;
    }
    .txt {
      font-size: 3vh;
    }
</style>
