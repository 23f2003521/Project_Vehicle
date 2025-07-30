<script>
import axios from 'axios';

export default {
  data() {
    return {
      profile:'',
      Message:''
    };
  },
  mounted() {
    this.getUserProfile();
  },
  methods: {
    getUserProfile: function(){
        const userId = this.$route.params.userid
        const response=axios.get(`http://127.0.0.1:5000/api/profile/${userId}`, {
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem("token")}`
  }
})
response
.then(res=>{
    console.log(res)
    this.profile=res.data
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
  <div class="container-fluid mt-2 px-5">
    
    <div v-if="profile">
      <div class="text-center mb-4">
  <i class="fas fa-user-circle fs-4"></i>

  <h3 class="mt-2">{{ profile.user.name }}</h3>
  <p class="text-muted">{{ profile.user.email }}</p>
  <!-- <router-link
    :to="`/user/edit/${userId}`"
    class="btn btn-primary mt-2"
  >
    Edit Profile
  </router-link> -->
</div>
<!-- User Stats Cards -->
<div class="row g-4 mt-4">
  <!-- Vehicle Number -->
  <div class="col-md-3">
    <div class="custom-card violet">
      <h6 class="fw-bold">Vehicle Number</h6>
      <h4>{{ profile.user.vehicle_no }}</h4>
    </div>
  </div>

  <!-- Total Reservations -->
  <div class="col-md-3">
    <div class="custom-card blue">
      <h6 class="fw-bold">Total Reservations</h6>
      <h4>{{ profile.total_reservations }}</h4>
    </div>
  </div>

  <!-- Active Reservations -->
  <div class="col-md-3">
    <div class="custom-card grey">
      <h6 class="fw-bold">Active Reservations</h6>
      <h4>{{ profile.active_reservations }}</h4>
    </div>
  </div>

  <!-- Total Amount Spent -->
  <div class="col-md-3">
    <div class="custom-card teal">
      <h6 class="fw-bold">Amount Spent</h6>
      <h4>₹{{ profile.total_amount_spent.toFixed(2) }}</h4>
    </div>
  </div>
</div>


      <hr />
      <h4 class="mb-3">Recent Reservations</h4>

<div class="table-responsive" style="max-height: 300px; overflow-y: auto;">
        <table class="table table-bordered table-striped table-hover" v-if="profile.recent_reservations.length">
          <thead class="table-light">
            <tr>
              <th>#</th>
              <th>Lot Name</th>
              <th>Spot ID</th>
              <th>Cost (₹)</th>
              <th>Status</th>
              <th>Parking Time</th>
              <th>Leaving Time</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(r, index) in profile.recent_reservations" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ r.lot_name }}</td>
              <td>{{ r.spot_id }}</td>
              <td>₹{{ r.parking_cost.toFixed(2) }}</td>
              <td>{{ r.reservation_status }}</td>
              <td>{{ r.parking_time }}</td>
              <td>{{ r.leaving_time }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else>No recent reservations available.</p>
      </div>

      
    </div>

    <div v-else>
      <p>No Data Available</p>
    </div>
  </div>
</template>





<style scoped>
.table-responsive {
  border: 1px solid #ddd;
  border-radius: 8px;
}

.card {
  transition: transform 0.2s;
}
.card:hover {
  transform: scale(1.03);
}
.stat-card {
  height: 150px;
  width: 100%;
  min-width: 200px;
}
.custom-card {
  height: 130px;
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.custom-card:hover {
  transform: translateY(-5px);
}

/* Gradient Themes */
.custom-card.violet {
  background: linear-gradient(135deg, #7E57C2, #6A1B9A);
}

.custom-card.blue {
  background: linear-gradient(135deg, #3D5AFE, #2962FF);
}

.custom-card.grey {
  background: linear-gradient(135deg, #B0BEC5, #90A4AE);
}

.custom-card.teal {
  background: linear-gradient(135deg, #00ACC1, #00838F);
}

</style>
