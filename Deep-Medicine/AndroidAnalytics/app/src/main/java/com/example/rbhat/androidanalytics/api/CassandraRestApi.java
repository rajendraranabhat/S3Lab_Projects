package com.example.rbhat.androidanalytics.api;

/**
 * Created by rbhat on 8/17/16.
 */



import com.example.rbhat.androidanalytics.model.Acceleration;
import com.example.rbhat.androidanalytics.model.TrainingAcceleration;

import retrofit.client.Response;
import retrofit.http.Body;
import retrofit.http.POST;

public interface CassandraRestApi {

    @POST("/acceleration")
    public Response sendAccelerationValues(@Body Acceleration acceleration);



    @POST("/training")
    public Response sendTrainingAccelerationValues(@Body TrainingAcceleration trainingAcceleration);


}
