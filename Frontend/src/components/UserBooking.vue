<script>
import axios from 'axios'
export default{
    data() {
        return{
            lotId:this.$route.params.lotid,
            FormData:{
                vehicle_no:'',
                parking_time:'',
                leaving_time:''
            },
            message:''
        }
    },
    methods: {
        bookSpot: function(){
            const response=axios.post(`http://127.0.0.1:5000/api/user/booking/${this.lotId}`, JSON.stringify(this.FormData),{
            headers:{
              'Content-Type': 'application/json',
              "Access-Control-Allow-Origin":"*",
              "Authorization": `Bearer ${localStorage.getItem("token")}`

            }
            })
            response
            .then(res=>{
              console.log(res)
               this.message=res.data.message
               this.$router.push("/dashboard")

            })
            .catch(err=>{
                this.message=err.response.data.message
                console.log(err)
              
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
        <form @submit.prevent="bookSpot">

          <div class="mb-3">
            <label class="form-label">Lot ID</label>
            <input  type="text" :value="lotId" disabled class="form-control" />
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
            <button type="submit" class="btn btn-primary btn-lg">Book Spot</button>
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












<style scoped>
label {
  font-weight: 500;
}
</style>