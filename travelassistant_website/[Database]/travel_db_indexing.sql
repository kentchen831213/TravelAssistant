
CREATE INDEX index_acc_id ON accommodations (Accommodation_id);
CREATE INDEX index_acc_city ON accommodations (city_name);
CREATE INDEX index_lan_city ON laundry (city_name);
CREATE INDEX index_acc_lat ON accommodations (latitude);
CREATE INDEX index_acc_lon ON accommodations (longitude);
CREATE INDEX index_acc_name ON accommodations (ac_name);
CREATE INDEX index_rm_id ON restaurants_comments (restaurant_id);
CREATE INDEX index_r_cat ON restaurants (category);
CREATE INDEX index_r_city ON restaurants (city_name);
CREATE INDEX index_ac_name ON accommodations (ac_name);
CREATE INDEX index_a_cat ON attractions (categories);