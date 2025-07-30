<script>
import axios from 'axios';
export default {
  data() {
    return {
      FormData: {
        prime_location_name: '',
        price_per_hour: '',
        address: '',
        pin_code: '',
        no_of_spot: ''
      },
      message: ''
    };
  },
  methods: {
    create_lot() {
      axios.post('http://127.0.0.1:5000/api/admin/create_lot', JSON.stringify(this.FormData), {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem('token')}`
        }
      })
      .then(res => {
        this.message = res.data.message || "Lot created successfully";
        setTimeout(() => this.$router.push('/dashboard'), 1000);
      })
      .catch(err => {
        this.message = err.response?.data?.message || "Something went wrong";
        console.error(err);
      });
    },
    resetForm() {
      this.FormData = {
        prime_location_name: '',
        price_per_hour: '',
        address: '',
        pin_code: '',
        no_of_spot: ''
      };
    }
  }
};
</script>

<template>
  <div class="container my-5">
    <div class="card shadow-lg p-4" style="max-height: 90vh; overflow: hidden;">
      <div class="form-scrollable" style="overflow-y: auto; flex: 1;">
        <h2 class="card-title text-center mb-4 text-primary">Create New Parking Lot</h2>

        <form @submit.prevent="create_lot">
          <div class="mb-3">
            <label class="form-label">Prime Location Name</label>
            <input type="text" v-model="FormData.prime_location_name" class="form-control" placeholder="e.g., MG Road, Sector 12" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Price Per Hour (₹)</label>
            <input type="number" v-model="FormData.price_per_hour" class="form-control" placeholder="e.g., 30" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Full Address</label>
            <input type="text" v-model="FormData.address" class="form-control" placeholder="Full parking lot address" required />
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Pin Code</label>
              <input type="text" v-model="FormData.pin_code" class="form-control" maxlength="6" placeholder="e.g., 110011" required />
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Number of Spots</label>
              <input type="number" v-model="FormData.no_of_spot" class="form-control" min="1" placeholder="e.g., 20" required />
            </div>
          </div>

          <div class="d-flex justify-content-between mt-4 gap-2">
            <RouterLink to="/dashboard" class="btn btn-outline-secondary fw-bold px-4 py-2 flex-fill text-center">
              <i class="fas fa-times"></i> Cancel
            </RouterLink>
            <button type="submit" class="btn btn-outline-primary fw-bold px-4 py-2 flex-fill">
              <i class="fas fa-plus-circle"></i> Create Lot
            </button>
          </div>
        </form>

        <p class="text-center mt-3 text-success">{{ message }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.form-scrollable {
  max-height: 75vh;
  overflow-y: auto;
}
</style>
