from trip_calculator.imp2.trip_controller import TripController, CostController

class TripHelper(TripController):

    def user_is_Trip_Owner(self, trip_id):
        trip = self.find_trip(trip_id)
        return trip.trip_owner.user_id == self.user_id

    def get_trip_squad(self, trip_id):
        for trip in self.trip_info:
            if trip_id == trip['trip_id']:
                return trip['squad']

    def get_all_trip_info(self):
        print(self.trip_info)
        return self.trip_info


class CostHelper(CostController):

    def get_all_cost_info(self, trip_id):
        pass







