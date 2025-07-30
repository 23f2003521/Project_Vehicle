<script>
import axios from 'axios'
export default {
  data() {
    return {
      spotId: this.$route.params.spotid,
      FormData: {
        spotId: '',
        status: '',
        lotId: '',
        address: '',
        username: '',
        vehicle_no: '',
        parking_time: '',
        leaving_time: '',
        parking_cost: ''
      },
      message: ''
    }
  },
  mounted() {
    this.fetchSpotData()
  },
  methods: {
    fetchSpotData: function() {
        const response = axios.get(`http://127.0.0.1:5000/api/admin/view_spot/${this.spotId}`, {
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('token')}`
          }
        });
            response
                .then(res=>{
                    const data = res.data

                    this.FormData = {
                    spotId: data.id,
                    status: data.status,
                    lotId: data.lot_id,
                    address: data.lot_address,
                    username: data.username || '',
                    vehicle_no: data.vehicle_no || '',
                    parking_time: data.parking_time || '',
                    leaving_time: data.leaving_time || '',
                    parking_cost: data.parking_cost || ''
        }
                }).catch(err=> {
                    console.log(err.response.data.message);
                })
      
    }
  }
}
</script>

<template>
  <div class="container my-5">
    <div class="card shadow-lg p-4" style="max-height: 90vh; overflow: hidden;">
      <div class="form-scrollable" style="overflow-y: auto; flex: 1;">
        <h2 class="card-title text-center mb-4 text-primary">Parking Spot Details</h2>
        
        <form>
          <div class="mb-3">
            <label class="form-label">Spot ID</label>
            <input type="text" class="form-control" :value="FormData.spotId" disabled>
          </div>

          <div class="mb-3">
            <label class="form-label">Status</label>
            <input type="text" class="form-control" :value="FormData.status" disabled>
          </div>

          <div class="mb-3">
            <label class="form-label">Lot ID</label>
            <input type="text" class="form-control" :value="FormData.lotId" disabled>
          </div>

          <div class="mb-3">
            <label class="form-label">Lot Address</label>
            <input type="text" class="form-control" :value="FormData.address" disabled>
          </div>

          <div v-if="FormData.username" class="mb-3">
            <label class="form-label">Username</label>
            <input type="text" class="form-control" :value="FormData.username" disabled>
          </div>

          <div v-if="FormData.vehicle_no" class="mb-3">
            <label class="form-label">Vehicle No.</label>
            <input type="text" class="form-control" :value="FormData.vehicle_no" disabled>
          </div>

          <div v-if="FormData.parking_time" class="mb-3">
            <label class="form-label">Parking Time</label>
            <input type="text" class="form-control" :value="FormData.parking_time" disabled>
          </div>

          <div v-if="FormData.leaving_time" class="mb-3">
            <label class="form-label">Leaving Time</label>
            <input type="text" class="form-control" :value="FormData.leaving_time" disabled>
          </div>

          <div v-if="FormData.parking_cost" class="mb-3">
            <label class="form-label">Parking Cost (₹)</label>
            <input type="text" class="form-control" :value="FormData.parking_cost" disabled>
          </div>
          <div class="d-flex justify-content-between mt-4 gap-2">
  <!-- Cancel Button -->
                <RouterLink to="/dashboard" class="btn btn-outline-secondary fw-bold rounded px-4 py-2 flex-fill text-center">
                <i class="fas fa-times"></i> Cancel
                </RouterLink>

  <!-- Delete Button -->
                <RouterLink :to="`/admin/delete_spot/${this.spotId}`" class="btn btn-outline-danger fw-bold rounded px-4 py-2 flex-fill text-center"><i class="fas fa-trash-alt"></i> Delete
                </RouterLink>
          </div>


        </form>

        <p class="text-danger text-center mt-3">{{ message }}</p>
      </div>
    </div>
  </div>
</template>
