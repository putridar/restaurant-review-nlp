<template>
  <div class="bg">
    <div class="left">
      <p class="name">{{this.name}}</p>
      <button class = "submit" v-on:click="navigate()">Try other restaurants!</button>
    </div>
    <div class="right">
      <p>{{result}} </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Sentiment',
  props: ['name'],
  data() {
    return {
      result: 'loading',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/scrape';
      axios.post(path, { name: this.name })
        .then((res) => {
          this.result = res.data;
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
        margin: 15px;
        margin-top: 30px;
        color: #1F335C;
    }
    .left {
      float: left;
      margin-left: 2%;
      width: 30%;
    }
    .right {
      margin-left: 35%;
      background: #e5e5e5;
      width: 60%;
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
        line-height: 44px;
        text-align: center;
        width: 80%;
        height: 60px;
        margin: 3%;
        cursor: pointer;
        transition-duration: 0.4s;
    }
</style>
