import { ref, computed, onMounted } from 'vue';
import CreateOrderService from '@/services/dss/users/customer';
import serviceTypesApi from '@/services/dss/serviceTypes';

type CustomerInfo = { id: string; name: string; phone_number?: string; address?: string; email?: string };
type ServiceType = { id: string; name: string; price_per_m2: number; description?: string };

type OrderFormData = {
  service_type: string;
  area_m2: number;
  requested_hours: number;
  preferred_start_time: Date | string;
  preferred_end_time: Date | string;
  estimated_hours: number;
  cost_confirm: number;
  payment_method: 'CASH' | 'BANK_TRANSFER';
  note: string;
};

export default function useCreateOrderViewModel(initialService?: Partial<ServiceType>) {
  const customerInfo = ref<CustomerInfo | null>(null);
  const serviceTypes = ref<ServiceType[]>([]);
  const selectedServiceType = ref<ServiceType | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const formData = ref<OrderFormData>({
    service_type: initialService?.id || '1fd520d16a2b45bf836269d5af828b60',
    area_m2: 20,
    requested_hours: 1,
    preferred_start_time: new Date().toISOString(),
    preferred_end_time: new Date(Date.now() + 3600000).toISOString(),
    estimated_hours: 1,
    cost_confirm: 0,
    payment_method: 'CASH',
    note: '',
  });

  const loadCustomerInfo = async () => {
    try {
      const resp = await CreateOrderService.getUser();
      const data = (resp && resp.data) ? resp.data : resp;
      customerInfo.value = data || null;
    } catch (err: any) {
      console.error('Error loading customer info (composable):', err);
      error.value = err?.message || 'Failed to load customer info';
    }
  };

  const loadServiceTypes = async () => {
    try {
      const resp = await serviceTypesApi.getAll?.();
      if (resp && resp.results) {
        serviceTypes.value = resp.results;
        if (!selectedServiceType.value && serviceTypes.value.length) {
          selectedServiceType.value = serviceTypes.value[0];
          formData.value.service_type = serviceTypes.value[0].id;
        }
        return;
      }
      // fallback: try getById
      const single = await serviceTypesApi.getServiceTypeById?.(formData.value.service_type as string);
      if (single && single.id) {
        const s: ServiceType = { id: single.id, name: single.name, price_per_m2: single.price_per_m2 || 0, description: single.description };
        serviceTypes.value = [s];
        selectedServiceType.value = s;
      }
    } catch (err: any) {
      console.error('Error loading service types (composable):', err);
      error.value = err?.message || 'Failed to load service types';
    }
  };

  const calculateEstimatedHours = (area: number) => {
    if (!area) return 0;
    // 1 hour per 20m2 (same as RN logic)
    return Math.ceil(area / 20);
  };

  const updateFormField = <K extends keyof OrderFormData>(field: K, value: OrderFormData[K]) => {
    formData.value = { ...formData.value, [field]: value } as OrderFormData;
  };

  const selectServiceType = (serviceTypeId: string) => {
    const s = serviceTypes.value.find(it => it.id === serviceTypeId) || null;
    selectedServiceType.value = s;
    if (s) formData.value.service_type = s.id;
  };

  const calculateTotalHours = () => {
    const start = new Date(formData.value.preferred_start_time as string).getTime();
    const end = new Date(formData.value.preferred_end_time as string).getTime();
    if (!start || !end || end <= start) return 0;
    return Math.round((end - start) / 3600000);
  };

  const createOrder = async (): Promise<{ success: boolean; order_id?: string; data?: any; paymentInfo?: any; error?: string }> => {
    if (!customerInfo.value) return { success: false, error: 'Customer not loaded' };
    loading.value = true; error.value = null;
    try {
      const payload: any = {
        customer: customerInfo.value.id,
        service_type: formData.value.service_type,
        area_m2: formData.value.area_m2,
        requested_hours: formData.value.requested_hours,
        preferred_start_time: (typeof formData.value.preferred_start_time === 'string') ? formData.value.preferred_start_time : (formData.value.preferred_start_time as Date).toISOString(),
        preferred_end_time: (typeof formData.value.preferred_end_time === 'string') ? formData.value.preferred_end_time : (formData.value.preferred_end_time as Date).toISOString(),
        estimated_hours: formData.value.estimated_hours,
        cost_confirm: Number(formData.value.cost_confirm),
        // mark as pending payment for bank transfer flow
        status: formData.value.payment_method === 'BANK_TRANSFER' ? 'PENDING_PAYMENT' : undefined,
        payment_method: formData.value.payment_method,
        note: formData.value.note,
      };

      const response = await CreateOrderService.createOrder(payload);
      const resp = response || {};
      // detect payment info
      const payment = resp.payment || resp.payment_info || resp.data?.payment || resp.data || null;
      if (payment) {
        return { success: true, order_id: resp.id || resp.order_id || '', data: resp, paymentInfo: payment };
      }
      return { success: true, order_id: resp.id || resp.order_id || '', data: resp };
    } catch (err: any) {
      console.error('Error creating order (composable):', err);
      const message = err?.message || 'Failed to create order';
      error.value = message;
      return { success: false, error: message };
    } finally {
      loading.value = false;
    }
  };

  onMounted(() => {
    loadCustomerInfo();
    loadServiceTypes();
  });

  return {
    customerInfo,
    serviceTypes,
    selectedServiceType,
    formData,
    loading,
    error,
    totalHours: computed(() => calculateTotalHours()),
    totalPrice: computed(() => formData.value.cost_confirm),
    updateFormField,
    selectServiceType,
    createOrder,
    refreshCustomerInfo: loadCustomerInfo,
    refreshServiceTypes: loadServiceTypes,
    calculateEstimatedHours,
  };
}
