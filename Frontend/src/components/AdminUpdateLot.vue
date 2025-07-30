<script>
import axios from 'axios';
export default{
    data() {
        return {
            lotId: this.$route.params.lotid,
            FormData : {
            prime_location_name: '',
            price_per_hour: '',
            address: '',
            pin_code: '',
            no_of_spot: ''

            },
            message:''
        }
    },
    mounted() {
    this.fetchLotData();
  },
    methods: {

        fetchLotData: function() {
        console.log(this.lotId)
        const response=axios.get(`http://127.0.0.1:5000/api/admin/get_lot/${this.lotId}`, {
        headers: {
          "Content-Type":"application/json",
          "Access-Control-Allow-Origin":"*",
          "Authorization": `Bearer ${localStorage.getItem('token')}`
        }
      })
      response
      .then(res => {
        this.FormData = res.data;
      })
      .catch(err => {
        
        console.error("Failed to fetch lot:", err.response?.data?.message);
      })
    },



        update_lot: function(){
            const response=axios.post(`http://127.0.0.1:5000/api/admin/update_lot/${this.lotId}`, JSON.stringify(this.FormData),{
            headers:{
              'Content-Type': 'application/json',
              "Access-Control-Allow-Origin":"*",
              "Authorization": `Bearer ${localStorage.getItem("token")}`

            }
            })
            response
            .then(res=> {
                this.message=res.data.message
                setTimeout(() => this.$router.push('/dashboard'), 1000);
            })
            .catch(err=> {
                    this.message=err.response.data.message
                    console.log(err);
                })

        }
    }
}
</script>

<template>
  <div class="container my-5">
    <div class="card shadow-lg p-4" style="max-height: 90vh; overflow: hidden;">
      
      <div class="form-scrollable" style="overflow-y: auto; flex: 1;" >
        <h2 class="card-title text-center mb-4 text-primary">Update Parking Lot</h2>
        <form @submit.prevent="update_lot">
          <div class="mb-3">
            <label for="prime_location_name" class="form-label">Prime Location Name</label>
            <input type="text" id="prime_location_name" v-model="FormData.prime_location_name" class="form-control" placeholder="Eg. MG Road, Sector 12" required>
          </div>

          <div class="mb-3">
            <label for="price_per_hour" class="form-label">Price Per Hour (₹)</label>
            <input type="number" id="price_per_hour" v-model="FormData.price_per_hour" class="form-control" placeholder="Eg. 30" required>
          </div>

          <div class="mb-3">
            <label for="address" class="form-label">Address</label>
            <input type="text" id="address" v-model="FormData.address" class="form-control" placeholder="Full address of parking lot" required>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="pin_code" class="form-label">Pin Code</label>
              <input type="text" id="pin_code" v-model="FormData.pin_code" class="form-control" placeholder="Eg. 110011" maxlength="6" required>
            </div>

            <div class="col-md-6 mb-3">
              <label for="no_of_spot" class="form-label">Number of Spots</label>
              <input type="number" id="no_of_spot" v-model="FormData.no_of_spot" class="form-control" placeholder="Eg. 20" min="1" required>
            </div>
          </div>

          <div class="text-center mt-4">
            <RouterLink to="/dashboard" class="btn btn-outline-secondary fw-bold rounded px-4 py-2 flex-fill text-center">
                <i class="fas fa-times"></i> Cancel
                </RouterLink>
            <button type="submit" class="btn btn-primary btn-lg">Update Lot</button>

          </div>
          <p>{{ message }}</p>
        </form>
      
      </div>
    </div>
  </div>
</template>



<style>

</style>