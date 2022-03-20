<template>
  <div class="bg">
    <p class="title1"> Restaurant Review</p>
    <p class = "title2"> Sentiment Analysis and Topic Modeling </p>
    <div class = "content">
        <p class = "label"> Enter a restaurant name </p>
        <input type="text" placeholder="Name" v-model="name" class ="inputstyle" required><br>
        <button class = "submit" v-on:click="navigate()">Submit</button>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Sentiment',
  data() {
    return {
      name: '',
    };
  },
  methods: {
    navigate() {
      this.$router.push({
        name: 'Sentiment',
        params: {
          name: this.name,
        },
      });
    },
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
    .title1 {
        font-family: Inter;
        font-style: normal;
        font-weight: bold;
        font-size: 44px;
        line-height: 58px;
        text-align: center;
        margin: 15px;
        margin-top: 30px;
    }
    .title2 {
        font-family: Inter;
        font-style: normal;
        font-weight: bold;
        font-size: 30px;
        line-height: 58px;
        text-align: center;
        margin: 15px;
    }
    .label {
        font-family: Inter;
        font-style: normal;
        font-weight: bold;
        font-size: 28px;
        line-height: 58px;
        text-align: center;
        margin: 15px;
    }
    .content {
        background-color: #E5E5E5;
        margin-top: 4%;
        margin-left: 35%;
        margin-right: 35%;
        height: 50%;
        width: 30%;
        justify-content: center;
        align-items: center;
        text-align: center;
        border-radius: 8px;
        padding: 10px;
        animation: zoomIn ease 0.7s
    }
    .inputstyle {
        font-family: Inter;
        padding: 8px;
        width: 80%;
        margin: 3%;
        font-size: 22px;
        border-radius: 8px;
        border: 1px solid #E5E5E5;
        height: 15%;
        margin-bottom: 7%;
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
