<script>
import axios from 'axios';

export default {
  data() {
    return {
      lotId: this.$route.params.lotid,
      message: '',
      lotDetails: null, // holds the lot details
    };
  },
  mounted() {
    this.fetchLotDetails();
  },
  methods: {
    fetchLotDetails() {
      axios
        .get(`http://127.0.0.1:5000/api/admin/get_lot/${this.lotId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem("token")}`
          }
        })
        .then(res => {
          this.lotDetails = res.data;
        })
        .catch(err => {
          this.message = err.response?.data?.message || "Failed to fetch lot details";
          console.error(err);
        });
    },

    deleteLot() {
      axios
        .delete(`http://127.0.0.1:5000/api/admin/delete_lot/${this.lotId}`, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("token")}`
          }
        })
        .then(res => {
          this.message = res.data.message;
          setTimeout(() => this.$router.push('/dashboard'), 1000);
        })
        .catch(err => {
          this.message = err.response?.data?.message || "An error occurred";
          console.error(err);
        });
    }
  }
};
</script>

<template>
  <div class="container mt-5">
    <h3>Delete Parking Lot</h3>

    <div v-if="lotDetails" class="mb-3">
      <p><strong>Location:</strong> {{ lotDetails.prime_location_name }}</p>
      <p><strong>Address:</strong> {{ lotDetails.address }}</p>
      <p><strong>Pincode:</strong> {{ lotDetails.pin_code }}</p>
      <p><strong>Spots:</strong> {{ lotDetails.no_of_spot }}</p>
      <p><strong>Price/Hour:</strong> ₹{{ lotDetails.price_per_hour }}</p>
    </div>
    
    <p class="text-success">{{ message }}</p>
    
    <button class="btn btn-danger" @click="deleteLot">Delete Lot</button>
  </div>
</template>
