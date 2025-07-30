
<script>
import axios from 'axios';

export default {
   data() {
    return {
        spotId: this.$route.params.spotid,
        message: ''
    }
  },
  methods: {
    deleteSpot: function() {
      const response=axios.get(`http://127.0.0.1:5000/api/admin/delete_spot/${this.spotId}`, {
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
        console.error(err);
      });
    }
  }
};
</script>


<template>
  <div class="container mt-5">
    <h3>Delete Parking Spot</h3>
    <p>{{ message }}</p>
    <button class="btn btn-danger" @click="deleteSpot">Delete Spot ID: {{ spotId }}</button>
  </div>
</template>
