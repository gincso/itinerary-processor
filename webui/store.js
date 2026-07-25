import { createStore } from "/js/AlpineStore.js";
import { toastFrontendSuccess, toastFrontendError } from "/components/notifications/notification-store.js";

export const store = createStore("itineraryStore", {
  processing: false,
  results: null,

  onOpen() {
    this.reset();
  },

  reset() {
    this.processing = false;
    this.results = null;
  },

  async handleUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    this.processing = true;

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`/api/itinerary_process?num_drivers=${this.numDrivers}`, {
        method: "POST",
        body: formData
      });

      if (!response.ok) throw new Error(await response.text());

      const data = await response.json();
      this.results = {
        csvUrl: data.csv_path,
        mapUrl: data.map_path
      };

      toastFrontendSuccess("Itinerary processed successfully", "Itinerary Processor");
    } catch (error) {
      toastFrontendError(`Processing failed: ${error.message}`, "Itinerary Processor");
    } finally {
      this.processing = false;
    }
  }
});

    initLiveMap() {
        // Called from Alpine init in the template
        if (typeof window.initLiveMap === 'function') {
            window.initLiveMap();
        }
    }
