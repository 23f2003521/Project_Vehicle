<script>
import axios from 'axios';
export default{
    data() {
        return {
            rvId: this.$route.params.reservationid,
            FormData : {
            lotId:'',
            vehicle_no:'',
            parking_time:'',
            leaving_time:'',
            userId:'',
            spotId:''

            },
            message:''
        }
    },
    mounted() {
    this.fetchReservationData();
  },
    methods: {

        fetchReservationData: function() {
        console.log(this.rvId)
        const response=axios.get(`http://127.0.0.1:5000/api/user/get_reservation/${this.rvId}`, {
        headers: {
          "Content-Type":"application/json",
          "Access-Control-Allow-Origin":"*",
          "Authorization": `Bearer ${localStorage.getItem('token')}`
        }
      })
      response
      .then(res => {
        this.FormData=res.data
        this.message=''
      })
      .catch(err => {
        this.message=err.response.data.message
        console.error("Failed to fetch spot:", err.response?.data?.message);
      })
    },



        update_booking: function(){
            const response=axios.post(`http://127.0.0.1:5000/api/user/update_booking/${this.rvId}`, JSON.stringify(this.FormData),{
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
        <h2 class="card-title text-center mb-4 text-primary">Book Parking Spot</h2>
        {{ message }}
        <form @submit.prevent="update_booking">

          <div class="mb-3">
            <label for="lotid" class="form-label">LotId</label>
            <input type="text" v-model="FormData.lotId" class="form-control" id="lotId" disabled/>
          </div>

          <div class="mb-3">
            <label for="spotid" class="form-label">SpotId</label>
            <input type="text" v-model="FormData.spotId" class="form-control" id="spotId" disabled/>
          </div>

          <div class="mb-3">
            <label for="userid" class="form-label">userId</label>
            <input type="text" v-model="FormData.userId" class="form-control" id="userId" disabled/>
          </div>
          

          <div class="mb-3">
            <label for="vehicle_no" class="form-label">Vehicle Number</label>
            <input type="text" v-model="FormData.vehicle_no" class="form-control" id="vehicle_no" required />
          </div>

          <div class="mb-3">
            <label for="parking_time" class="form-label">Parking Time</label>
            <input type="datetime-local" v-model="FormData.parking_time" class="form-control" id="parking_time" required />
          </div>


          <div class="mb-3">
            <label for="leaving_time" class="form-label">Leaving Time</label>
            <input type="datetime-local" v-model="FormData.leaving_time" class="form-control" id="leaving_time" required />
          </div>

          <div class="text-center mt-4">
            <button type="submit" class="btn btn-primary btn-lg">Update Booking</button>
          </div>
          <RouterLink to="/dashboard" class="btn btn-outline-secondary fw-bold rounded px-4 py-2 flex-fill text-center">
                <i class="fas fa-times"></i> Cancel
                </RouterLink>
        </form>

        <div v-if="message" class="mt-4 alert" :class="{'alert-success': success, 'alert-danger': !success}">
        {{ message }}
        </div>
      
      </div>
    </div>
  </div>
</template>




<style>

</style>