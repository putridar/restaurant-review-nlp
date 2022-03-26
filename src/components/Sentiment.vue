<template>
  <div class="bg">
    <div class="left">
      <p class="name">{{this.name}}</p><br><br>
      <p> Frequent Words: </p>
      <vue-word-cloud
      style="height: 30vh; width: 30vw"
      :words="ws"
    >
      <template slot-scope="{ text, weight, word }">
        <div :title="weight" style="cursor: pointer" @click="onWordClick(word)">
          {{ text }}
        </div>
      </template></vue-word-cloud
    >
      <button class = "submit" v-on:click="navigate()">Try other restaurants!</button>
    </div>
    <div class="right">
      <p>{{this.result}}</p>
      <Chart></Chart>
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
      ws: [],
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/scrape';
      axios.post(path, { name: this.name })
        .then((res) => {
          this.result = res.data;
          const r = this.result.map((e) => {
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
    onWordClick(text) {
      alert(text.text);
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
      background: #e5e5e5;
      width: 55vw;
      border-radius: 8px;
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
    }
</style>
