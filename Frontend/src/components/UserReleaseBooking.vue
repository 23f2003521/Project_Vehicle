
<script>
import axios from 'axios';

export default {
   data() {
    return {
        resId: this.$route.params.reservationid,
        message: ''
    }
  },
  methods: {
    releaseSpot: function() {
      console.log(this.resId)
      const response=axios.get(`http://127.0.0.1:5000/api/user/release_booking/${this.resId}`, {
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem("token")}`
  }
})
response
.then(res=>{
        console.log(res)
        this.message=res.data.message
        setTimeout(() => this.$router.push('/dashboard'), 1000);
      })
      .catch(err => {
        this.Message = err.response?.data?.message || "An error occurred";
        console.log(err)
      });
    }
  }
};
</script>


<template>
  <div class="container mt-5">
    <h3>Release Parking Spot</h3>
    <p>{{ message }}</p>
    <button class="btn btn-danger" @click="releaseSpot">Release Spot</button>
  </div>
</template>
