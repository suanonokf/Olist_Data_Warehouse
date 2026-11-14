from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class DimGeolocation(Base):
    __tablename__ = 'dim_geolocations'
    zip_code_prefix = Column(String(5), primary_key=True)
    city = Column(String)
    state = Column(String(2))

class DimDate(Base):
    __tablename__ = 'dim_dates'
    date_key = Column(Integer, primary_key=True)
    full_date = Column(Date, nullable=False, unique=True)
    year = Column(Integer)
    quarter = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    day_of_week = Column(Integer)

class DimCustomer(Base):
    __tablename__ = 'dim_customers'
    customer_id = Column(String(32), primary_key=True)
    customer_unique_id = Column(String(32), index=True)
    zip_code_prefix = Column(String(5), ForeignKey('dim_geolocations.zip_code_prefix'))

class DimSeller(Base):
    __tablename__ = 'dim_sellers'
    seller_id = Column(String(32), primary_key=True)
    zip_code_prefix = Column(String(5), ForeignKey('dim_geolocations.zip_code_prefix'))

class DimProduct(Base):
    __tablename__ = 'dim_products'
    product_id = Column(String(32), primary_key=True)
    category_name = Column(String)
    weight_g = Column(Numeric)
    length_cm = Column(Numeric)
    height_cm = Column(Numeric)
    width_cm = Column(Numeric)

class DimReview(Base):
    __tablename__ = 'dim_reviews'
    review_id = Column(String(32), primary_key=True)
    review_score = Column(Integer)

class FactOrderItem(Base):
    __tablename__ = 'fact_order_items'
    order_id = Column(String(32), primary_key=True)
    order_item_id = Column(Integer, primary_key=True)

    customer_id = Column(String(32), ForeignKey('dim_customers.customer_id'), nullable=False)
    product_id = Column(String(32), ForeignKey('dim_products.product_id'), nullable=False)
    seller_id = Column(String(32), ForeignKey('dim_sellers.seller_id'), nullable=False)
    review_id = Column(String(32), ForeignKey('dim_reviews.review_id'))
    purchase_date_key = Column(Integer, ForeignKey('dim_dates.date_key'))
    delivery_date_key = Column(Integer, ForeignKey('dim_dates.date_key'))

    price = Column(Numeric(10, 2))
    freight_value = Column(Numeric(10, 2))
    order_status = Column(String)

    purchase_date = relationship('DimDate', foreign_keys=[purchase_date_key])
    delivery_date = relationship('DimDate', foreign_keys=[delivery_date_key])