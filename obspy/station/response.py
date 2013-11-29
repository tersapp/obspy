#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Classes related to instrument responses.

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2013
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)
"""
from obspy.core.util.base import ComparingObject


class ResponseStage(ComparingObject):
    """
    From the StationXML Definition:
        This complex type represents channel response and covers SEED
        blockettes 53 to 56.
    """
    def __init__(self, stage_sequence_number, stage_gain_value,
                 stage_gain_frequency, input_units, output_units,
                 resource_id, name, input_units_description=None,
                 output_units_description=None, description=None,
                 decimation_input_sample_rate=None, decimation_factor=None,
                 decimation_offset=None, decimation_delay=None,
                 decimation_correction=None):
        """
        :type stage_sequence_number: integer greater or equal to zero
        :param stage_sequence_number: Stage sequence number. This is used in
            all the response SEED blockettes.
        :type stage_gain_value: float
        :param stage_gain_value: Complex type for sensitivity and frequency
            ranges. This complex type can be used to represent both overall
            sensitivities and individual stage gains.  A scalar that, when
            applied to the data values, converts the data to different units
            (e.g. Earth units).
        :type stage_gain_frequency: float
        :param stage_gain_frequency: Complex type for sensitivity and frequency
            ranges. This complex type can be used to represent both overall
            sensitivities and individual stage gains. The frequency (in Hertz)
            at which the Value is valid.
        :param input_units: string
        :param input_units: The units of the data as input from the
            perspective of data acquisition. After correcting data for this
            response, these would be the resulting units.
            Name of units, e.g. "M/S", "V", "PA".
        :param output_units: string
        :param output_units: The units of the data as output from the
            perspective of data acquisition. These would be the units of the
            data prior to correcting for this response.
            Name of units, e.g. "M/S", "V", "PA".
        :type resource_id: string
        :param resource_id: This field contains a string that should serve as a
            unique resource identifier. This identifier can be interpreted
            differently depending on the datacenter/software that generated the
            document. Also, we recommend to use something like
            GENERATOR:Meaningful ID. As a common behaviour equipment with the
            same ID should contains the same information/be derived from the
            same base instruments.
        :type name: string
        :param name: A name given to the filter stage.
        :param input_units_description: string, optional
        :param input_units_description: The units of the data as input from the
            perspective of data acquisition. After correcting data for this
            response, these would be the resulting units.
            Description of units, e.g. "Velocity in meters per second",
            "Volts", "Pascals".
        :type output_units_description: string, optional
        :param output_units_description: The units of the data as output from
            the perspective of data acquisition. These would be the units of
            the data prior to correcting for this response.
            Description of units, e.g. "Velocity in meters per second",
            "Volts", "Pascals".
        :type description: string, optional
        :param description: A short description of of the filter.
        :type decimation_input_sample_rate:  float, optional
        :param decimation_input_sample_rate: The sampling rate before the
            decimation in samples per second.
        :type decimation_factor: integer, optional
        :param decimation_factor: The applied decimation factor.
        :type decimation_offset: integer, optional
        :param decimation_offset: The sample chosen for use. 0 denotes the
            first sample, 1 the second, and so forth.
        :type decimation_delay: float, optional
        :param decimation_delay: The estimated pure delay from the decimation.
        :type decimation_correction: float, optional
        :param decimation_correction: The time shift applied to correct for the
            delay at this stage.

        .. note::
            The stage gain (or stage sensitivity) is the gain at the stage of
            the encapsulating response element and corresponds to SEED
            blockette 58. In the SEED convention, stage 0 gain represents the
            overall sensitivity of the channel.  In this schema, stage 0 gains
            are allowed but are considered deprecated.  Overall sensitivity
            should be specified in the InstrumentSensitivity element.
        """
        self.stage_sequence_number = stage_sequence_number
        self.input_units = input_units
        self.output_units = output_units
        self.input_units_description = input_units_description
        self.output_units_description = output_units_description
        self.resource_id = resource_id
        self.stage_gain_value = stage_gain_value
        self.stage_gain_frequency = stage_gain_frequency
        self.name = name
        self.description = description
        self.decimation_input_sample_rate = decimation_input_sample_rate
        self.decimation_factor = decimation_factor
        self.decimation_offset = decimation_offset
        self.decimation_delay = decimation_delay
        self.decimation_correction = decimation_correction

    def __str__(self):
        ret = (
            "Response type: {response_type}, Stage Sequence Number: "
            "{response_stage}\n"
            "{name_desc}"
            "{resource_id}"
            "\tFrom {input_units}{input_desc} to {output_units}{output_desc}\n"
            "\tStage gain: {gain_value}, defined at {gain_freq:.2f} Hz\n"
            "{decimation}").format(
            response_type=self.__class__.__name__,
            response_stage=self.stage_sequence_number,
            name_desc="\t%s %s\n" % (
                self.name, "(%s)" % self.description
                if self.description else "") if self.name else "",
            resource_id="\tResource Id: %s" % self.resource_id
            if self.resource_id else "",
            input_units=self.input_units,
            input_desc=" (%s)" % self.input_units_description
            if self.input_units_description else "",
            output_units=self.output_units,
            output_desc=" (%s)" % self.output_units_description
            if self.output_units_description else "",
            gain_value=self.stage_gain_value,
            gain_freq=self.stage_gain_frequency,
            decimation=
            "\tDecimation:\n\t\tInput Sample Rate: %.2f Hz\n\t\t"
            "Decimation Factor: %i\n\t\tDecimation Offset: %i\n\t\t"
            "Decimation Delay: %.2f\n\t\tDecimation Correction: %.2f" % (
                self.decimation_input_sample_rate, self.decimation_factor,
                self.decimation_offset, self.decimation_delay,
                self.decimation_correction)
            if self.decimation_input_sample_rate is not None else "")
        return ret.strip()


class PolesZerosResponseStage(ResponseStage):
    """
    From the StationXML Definition:
        Response: complex poles and zeros. Corresponds to SEED blockette 53.

    The response stage is used for the analog stages of the filter system and
    the description of infinite impulse response (IIR) digital filters.

    Has all the arguments of the parent class
    :class:`~obspy.station.response.ResponseStage` and the following:

    :type pz_transfer_function_type: String
    :param pz_transfer_function_type: A string describing the type of transfer
        function. Can be one of:
            * ``LAPLACE (RADIANS/SECOND)``
            * ``LAPLACE (HERTZ)``
            * ``DIGITAL (Z-TRANSFORM)``
        The function tries to match inputs to one of three types if it can.
    :type normalization_frequency: float
    :param normalization_frequency: The frequency at which the normalization
        factor is normalized.
    :type zeros: A list of complex numbers.
    :param zeros: All zeros of the stage.
    :type poles: A list of complex numbers.
    :param poles: All poles of the stage.
    :type normalization_factor: float, optional
    :param normalization_factor:
    """
    def __init__(self, stage_sequence_number, stage_gain_value,
                 stage_gain_frequency, input_units, output_units,
                 resource_id, name, pz_transfer_function_type,
                 normalization_frequency, zeros, poles,
                 normalization_factor=1.0, input_units_description=None,
                 output_units_description=None, description=None,
                 decimation_input_sample_rate=None, decimation_factor=None,
                 decimation_offset=None, decimation_delay=None,
                 decimation_correction=None):
        # Set the Poles and Zeros specific attributes. Special cases are
        # handled by properties.
        self.pz_transfer_function_type = pz_transfer_function_type
        self.normalization_frequency = float(normalization_frequency)
        self.normalization_factor = float(normalization_factor)
        self.zeros = zeros
        self.poles = poles
        super(PolesZerosResponseStage, self).__init__(
            stage_sequence_number=stage_sequence_number,
            input_units=input_units,
            output_units=output_units,
            input_units_description=input_units_description,
            output_units_description=output_units_description,
            resource_id=resource_id, stage_gain_value=stage_gain_value,
            stage_gain_frequency=stage_gain_frequency, name=name,
            description=description,
            decimation_input_sample_rate=decimation_input_sample_rate,
            decimation_factor=decimation_factor,
            decimation_offset=decimation_offset,
            decimation_delay=decimation_delay,
            decimation_correction=decimation_correction)

    def __str__(self):
        ret = super(PolesZerosResponseStage, self).__str__()
        ret += (
            "\n"
            "\tTransfer function type: {transfer_fct_type}\n"
            "\tNormalization factor: {norm_fact:g}, "
            "Normalization frequency: {norm_freq:.2f} Hz\n"
            "\tPoles: {poles}\n"
            "\tZeros: {zeros}").format(
            transfer_fct_type=self.pz_transfer_function_type,
            norm_fact=self.normalization_factor,
            norm_freq=self.normalization_frequency,
            poles=", ".join(map(str, self.poles)),
            zeros=", ".join(map(str, self.zeros)),
            )
        return ret

    @property
    def zeros(self):
        return self.__zeros

    @zeros.setter
    def zeros(self, value):
        self.__zeros = map(complex, value)

    @property
    def poles(self):
        return self.__poles

    @poles.setter
    def poles(self, value):
        self.__poles = map(complex, value)

    @property
    def pz_transfer_function_type(self):
        return self.__pz_transfer_function_type

    @pz_transfer_function_type.setter
    def pz_transfer_function_type(self, value):
        """
        Setter for the transfer function type.

        Rather permissive but should make it less awkward to use.
        """
        msg = ("'%s' is not a valid value for 'pz_transfer_function_type'. "
               "Valid one are:\n"
               "\tLAPLACE (RADIANS/SECOND)\n"
               "\tLAPLACE (HERTZ)\n"
               "\tDIGITAL (Z-TRANSFORM)") % value
        value = value.lower()
        if "laplace" in value:
            if "radian" in value:
                self.__pz_transfer_function_type = "LAPLACE (RADIANS/SECOND)"
            elif "hertz" in value or "hz" in value:
                self.__pz_transfer_function_type = "LAPLACE (HERTZ)"
            else:
                raise ValueError(msg)
        elif "digital" in value:
            self.__pz_transfer_function_type = "DIGITAL (Z-TRANSFORM)"
        else:
            raise ValueError(msg)


class CoefficientsTypeResponseStage(ResponseStage):
    """
    This response type can describe coefficients for FIR filters. Laplace
    transforms and IIR filters can also be expressed using this type but should
    rather be described using the PolesZerosResponseStage class. Effectively
    corresponds to SEED blockette 54.

    Has all the arguments of the parent class
    :class:`~obspy.station.response.ResponseStage` and the following:

    :type cf_transfer_function_type: String
    :param cf_transfer_function_type: A string describing the type of transfer
        function. Can be one of:
            * ``ANALOG (RADIANS/SECOND)``
            * ``ANALOG (HERTZ)``
            * ``DIGITAL``
        The function tries to match inputs to one of three types if it can.
    :type numerator: list of float
    :param numerator:
    :type denominator: list of float
    :param denominator:
    """
    def __init__(self, stage_sequence_number, stage_gain_value,
                 stage_gain_frequency, input_units, output_units,
                 resource_id, name, cf_transfer_function_type, numerator=None,
                 denominator=None, input_units_description=None,
                 output_units_description=None, description=None,
                 decimation_input_sample_rate=None, decimation_factor=None,
                 decimation_offset=None, decimation_delay=None,
                 decimation_correction=None):
        # Set the Coefficients type specific attributes. Special cases are
        # handled by properties.
        self.cf_transfer_function_type = cf_transfer_function_type
        self.numerator = numerator
        self.denominator = denominator
        super(CoefficientsTypeResponseStage, self).__init__(
            stage_sequence_number=stage_sequence_number,
            input_units=input_units,
            output_units=output_units,
            input_units_description=input_units_description,
            output_units_description=output_units_description,
            resource_id=resource_id, stage_gain_value=stage_gain_value,
            stage_gain_frequency=stage_gain_frequency, name=name,
            description=description,
            decimation_input_sample_rate=decimation_input_sample_rate,
            decimation_factor=decimation_factor,
            decimation_offset=decimation_offset,
            decimation_delay=decimation_delay,
            decimation_correction=decimation_correction)

    def __str__(self):
        ret = super(CoefficientsTypeResponseStage, self).__str__()
        ret += (
            "\n"
            "\tTransfer function type: {transfer_fct_type}\n"
            "\tContains {num_count} numerators and {den_count} denominators")\
            .format(
                transfer_fct_type=self.cf_transfer_function_type,
                num_count=len(self.numerator), den_count=len(self.denominator))
        return ret

    @property
    def numerator(self):
        return self.__numerator

    @numerator.setter
    def numerator(self, value):
        if value is None:
            self.__numerator = []
            return
        self.__numerator = map(float, value)

    @property
    def denominator(self):
        return self.__denominator

    @denominator.setter
    def denominator(self, value):
        if value is None:
            self.__denominator = []
            return
        self.__denominator = map(float, value)

    @property
    def cf_transfer_function_type(self):
        return self.__cf_transfer_function_type

    @cf_transfer_function_type.setter
    def cf_transfer_function_type(self, value):
        """
        Setter for the transfer function type.

        Rather permissive but should make it less awkward to use.
        """
        msg = ("'%s' is not a valid value for 'cf_transfer_function_type'. "
               "Valid one are:\n"
               "\tANALOG (RADIANS/SECOND)\n"
               "\tANALOG (HERTZ)\n"
               "\tDIGITAL") % value
        value = value.lower()
        if "analog" in value:
            if "radian" in value:
                self.__cf_transfer_function_type = "ANALOG (RADIANS/SECOND)"
            elif "hertz" in value or "hz" in value:
                self.__cf_transfer_function_type = "ANALOG (HERTZ)"
            else:
                raise ValueError(msg)
        elif "digital" in value:
            self.__cf_transfer_function_type = "DIGITAL"
        else:
            raise ValueError(msg)


class ResponseListResponseStage(ResponseStage):
    """
    This response type gives a list of frequency, amplitude and phase value
    pairs. Effectively corresponds to SEED blockette 55.

    Has all the arguments of the parent class
    :class:`~obspy.station.response.ResponseStage` and the following:

    :type response_list_elements: list of
        :class:`~obspy.station.response.ResponseListElement`
    :param response_list_elements: A list of single discrete frequency,
        amplitude and phase response values.
    """
    def __init__(self, stage_sequence_number, stage_gain_value,
                 stage_gain_frequency, input_units, output_units,
                 resource_id, name, response_list_elements=None,
                 input_units_description=None, output_units_description=None,
                 description=None, decimation_input_sample_rate=None,
                 decimation_factor=None, decimation_offset=None,
                 decimation_delay=None, decimation_correction=None):
        self.response_list_elements = response_list_elements or []
        super(ResponseListResponseStage, self).__init__(
            stage_sequence_number=stage_sequence_number,
            input_units=input_units,
            output_units=output_units,
            input_units_description=input_units_description,
            output_units_description=output_units_description,
            resource_id=resource_id, stage_gain_value=stage_gain_value,
            stage_gain_frequency=stage_gain_frequency, name=name,
            description=description,
            decimation_input_sample_rate=decimation_input_sample_rate,
            decimation_factor=decimation_factor,
            decimation_offset=decimation_offset,
            decimation_delay=decimation_delay,
            decimation_correction=decimation_correction)


class ResponseListElement(ComparingObject):
    """
    Describes the amplitude and phase response value for a discrete frequency
    value.
    """
    def __init__(self, frequency, amplitude, phase):
        """
        :type frequency: float
        :param frequency: The frequency for which the response is valid.
        :type amplitude: float
        :param amplitude: The value for the amplitude response at this
            frequency.
        :type phase: float
        :param phase: The value for the phase response at this frequency.
        """
        self.frequency = frequency
        self.amplitude = amplitude
        self._phase = phase

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        value = float(value)
        if not -360 <= value <= 360:
            raise ValueError("Phase angle out of allowed range.")
        self._phase = value


class FIRResponseStage(ResponseStage):
    """
    From the StationXML Definition:
        Response: FIR filter. Corresponds to SEED blockette 61. FIR filters are
        also commonly documented using the CoefficientsType element.

    Has all the arguments of the parent class
    :class:`~obspy.station.response.ResponseStage` and the following:

    :type symmetry: String
    :param symmetry: A string describing the symmetry. Can be one of:
            * ``NONE``
            * ``EVEN``
            * ``ODD``
    :type numerator_coefficients: list of floats
    :param numerator_coefficients: List of numerator coefficients.
    """
    def __init__(self, stage_sequence_number, stage_gain_value,
                 stage_gain_frequency, input_units, output_units,
                 resource_id, name, symmetry="NONE",
                 numerator_coefficients=None, input_units_description=None,
                 output_units_description=None, description=None,
                 decimation_input_sample_rate=None, decimation_factor=None,
                 decimation_offset=None, decimation_delay=None,
                 decimation_correction=None):
        self._symmetry = symmetry
        self.numerator_coefficients = numerator_coefficients or []
        super(FIRResponseStage, self).__init__(
            stage_sequence_number=stage_sequence_number,
            input_units=input_units,
            output_units=output_units,
            input_units_description=input_units_description,
            output_units_description=output_units_description,
            resource_id=resource_id, stage_gain_value=stage_gain_value,
            stage_gain_frequency=stage_gain_frequency, name=name,
            description=description,
            decimation_input_sample_rate=decimation_input_sample_rate,
            decimation_factor=decimation_factor,
            decimation_offset=decimation_offset,
            decimation_delay=decimation_delay,
            decimation_correction=decimation_correction)

    @property
    def symmetry(self):
        return self._symmetry

    @symmetry.setter
    def symmetry(self, value):
        value = str(value).upper()
        allowed = ("NONE", "EVEN", "ODD")
        if value not in allowed:
            msg = ("Value '%s' for FIR Response symmetry not allowed. "
                   "Possible values are: '%s'")
            msg = msg % (value, "', '".join(allowed))
            raise ValueError(msg)
        self._symmetry = value


class PolynomialResponseStage(ResponseStage):
    """
    From the StationXML Definition:
        Response: expressed as a polynomial (allows non-linear sensors to be
        described). Corresponds to SEED blockette 62. Can be used to describe a
        stage of acquisition or a complete system.

    Has all the arguments of the parent class
    :class:`~obspy.station.response.ResponseStage` and the following:

    :type approximation_type: str
    :param approximation_type: Approximation type. Currently restricted to
        'MACLAURIN' by StationXML definition.
    :type frequency_lower_bound: float
    :param frequency_lower_bound: Lower frequency bound.
    :type frequency_upper_bound: float
    :param frequency_upper_bound: Upper frequency bound.
    :type approximation_lower_bound: float
    :param approximation_lower_bound: Lower bound of approximation.
    :type approximation_upper_bound: float
    :param approximation_upper_bound: Upper bound of approximation.
    :type maximum_error: float
    :param maximum_error: Maximum error.
    :type coefficients: list of floats
    :param coefficients: List of polynomial coefficients.
    """
    def __init__(self, stage_sequence_number, stage_gain_value,
                 stage_gain_frequency, input_units, output_units,
                 resource_id, name, frequency_lower_bound,
                 frequency_upper_bound, approximation_lower_bound,
                 approximation_upper_bound, maximum_error, coefficients,
                 approximation_type='MACLAURIN',
                 input_units_description=None,
                 output_units_description=None, description=None,
                 decimation_input_sample_rate=None, decimation_factor=None,
                 decimation_offset=None, decimation_delay=None,
                 decimation_correction=None):
        self._approximation_type = approximation_type
        self.frequency_lower_bound = frequency_lower_bound
        self.frequency_upper_bound = frequency_upper_bound
        self.approximation_lower_bound = approximation_lower_bound
        self.approximation_upper_bound = approximation_upper_bound
        self.maximum_error = maximum_error
        self.coefficients = coefficients
        super(PolynomialResponseStage, self).__init__(
            stage_sequence_number=stage_sequence_number,
            input_units=input_units,
            output_units=output_units,
            input_units_description=input_units_description,
            output_units_description=output_units_description,
            resource_id=resource_id, stage_gain_value=stage_gain_value,
            stage_gain_frequency=stage_gain_frequency, name=name,
            description=description,
            decimation_input_sample_rate=decimation_input_sample_rate,
            decimation_factor=decimation_factor,
            decimation_offset=decimation_offset,
            decimation_delay=decimation_delay,
            decimation_correction=decimation_correction)

    @property
    def approximation_type(self):
        return self._approximation_type

    @approximation_type.setter
    def approximation_type(self, value):
        value = str(value).upper()
        allowed = ("MACLAURIN",)
        if value not in allowed:
            msg = ("Value '%s' for polynomial response approximation type not "
                   "allowed. Possible values are: '%s'")
            msg = msg % (value, "', '".join(allowed))
            raise ValueError(msg)
        self._approximation_type = value


class Response(ComparingObject):
    """
    The root response object.
    """
    def __init__(self, resource_id=None, instrument_sensitivity=None,
                 response_stages=None):
        """
        :type resource_id: string
        :param resource_id: This field contains a string that should serve as a
            unique resource identifier. This identifier can be interpreted
            differently depending on the datacenter/software that generated the
            document. Also, we recommend to use something like
            GENERATOR:Meaningful ID. As a common behaviour equipment with the
            same ID should contains the same information/be derived from the
            same base instruments.
        :type instrument_sensitivity:
            :class:`~obspy.station.response.InstrumentSensitivity`
        :param instrument_sensitivity: The total sensitivity for the given
            channel.
        :type response_stages: List of
            :class:`~obspy.station.response.ResponseStage` objects
        :param response_stages: A list of the response stages. Covers SEED
            blockettes 53 to 56.
        """
        self.resource_id = resource_id
        self.instrument_sensitivity = instrument_sensitivity
        if response_stages is None:
            self.response_stages = []
        elif hasattr(response_stages, "__iter__"):
            self.response_stages = response_stages
        else:
            msg = "response_stages must be an iterable."
            raise ValueError(msg)

    def get_evalresp_response(self, t_samp, nfft):
        import ctypes as C
        import numpy as np
        import obspy.signal.evrespwrapper as ew
        from collections import defaultdict
        from obspy.signal.headers import clibevresp

        # Whacky. Evalresp uses a global variable and uses that to scale the
        # response if it encounters any unit that is not SI.
        scale_factor = [1.0]

        def get_unit_mapping(key):
            units_mapping = {
                "M": ew.ENUM_UNITS["DIS"],
                "NM": ew.ENUM_UNITS["DIS"],
                "CM": ew.ENUM_UNITS["DIS"],
                "MM": ew.ENUM_UNITS["DIS"],
                "M/S": ew.ENUM_UNITS["VEL"],
                "NM/S": ew.ENUM_UNITS["VEL"],
                "CM/S": ew.ENUM_UNITS["VEL"],
                "MM/S": ew.ENUM_UNITS["VEL"],
                "M/S**2": ew.ENUM_UNITS["ACC"],
                "NM/S**2": ew.ENUM_UNITS["ACC"],
                "CM/S**2": ew.ENUM_UNITS["ACC"],
                "MM/S**2": ew.ENUM_UNITS["ACC"],
                "V": ew.ENUM_UNITS["VOLTS"],
                "COUNTS": ew.ENUM_UNITS["COUNTS"],
                "PA": ew.ENUM_UNITS["PRESSURE"]}
            if key not in units_mapping:
                value = ew.ENUM_UNITS["UNDEF_UNITS"]
            else:
                value = units_mapping[key]

            # Scale factor with the same logic as evalresp.
            if key in ["CM/S**2", "CM/S*2"]:
                scale_factor[0] = 1.0E2
            elif key in ["MM/S**2", "MM/S*2"]:
                scale_factor[0] = 1.0E3
            elif key in ["NM/S**2", "NM/S*2"]:
                scale_factor[0] = 1.0E9

            return value

        all_stages = defaultdict(list)

        for stage in self.response_stages:
            all_stages[stage.stage_sequence_number].append(stage)

        stage_lengths = set(map(len, all_stages.values()))
        if len(stage_lengths) != 1 or stage_lengths.pop() != 1:
            msg = "Each stage can only appear once."
            raise ValueError(msg)

        stage_list = sorted(all_stages.keys())

        stage_objects = []

        for stage_number in stage_list:
            st = ew.stage()
            st.sequence_no = stage_number

            stage_blkts = []

            blkt = ew.blkt()

            blockette = all_stages[stage_number][0]

            # Write the input and output units.
            st.input_units = get_unit_mapping(blockette.input_units)
            st.output_units = get_unit_mapping(blockette.output_units)

            if isinstance(blockette, PolesZerosResponseStage):
                # Map the transfer function type.
                transfer_fct_mapping = {
                    "LAPLACE (RADIANS/SECOND)": "LAPLACE_PZ",
                    "LAPLACE (HERTZ)": "ANALOG_PZ",
                    "DIGITAL (Z-TRANSFORM)": "IIR_PZ"}
                blkt.type = ew.ENUM_FILT_TYPES[transfer_fct_mapping[
                    blockette.pz_transfer_function_type]]

                # The blockette is a pole zero blockette.
                pz = blkt.blkt_info.pole_zero

                pz.nzeros = len(blockette.zeros)
                pz.npoles = len(blockette.poles)
                pz.a0 = blockette.normalization_factor
                pz.a0_freq = blockette.normalization_frequency

                # XXX: Find a better way to do this.
                poles = (ew.complex_number * len(blockette.poles))()
                for i, value in enumerate(blockette.poles):
                    poles[i].real = value.real
                    poles[i].imag = value.imag

                zeros = (ew.complex_number * len(blockette.zeros))()
                for i, value in enumerate(blockette.zeros):
                    zeros[i].real = value.real
                    zeros[i].imag = value.imag

                pz.poles = C.cast(C.pointer(poles),
                                  C.POINTER(ew.complex_number))
                pz.zeros = C.cast(C.pointer(zeros),
                                  C.POINTER(ew.complex_number))
            elif isinstance(blockette, CoefficientsTypeResponseStage):
                # This type can have either an FIR or an IIR response. If
                # the number of denominators is 0, it is a FIR. Otherwise
                # an IIR.

                # FIR
                if len(blockette.denominator) == 0:
                    if blockette.cf_transfer_function_type.lower() \
                            != "digital":
                        msg = ("When no denominators are given it must "
                               "be a digital FIR filter.")
                        raise ValueError(msg)
                    # Set the type to an assymetric FIR blockette.
                    blkt.type = ew.ENUM_FILT_TYPES["FIR_ASYM"]
                    fir = blkt.blkt_info.fir
                    fir.h0 = 1.0
                    fir.ncoeffs = len(blockette.numerator)
                    # XXX: Find a better way to do this.
                    coeffs = (C.c_double * len(blockette.numerator))()
                    for i, value in enumerate(blockette.numerator):
                        coeffs[i] = float(value)
                    fir.coeffs = C.cast(C.pointer(coeffs),
                                        C.POINTER(C.c_double))
                # IIR
                else:
                    raise NotImplementedError
            else:
                msg = "Type: %s." % str(type(blockette))
                raise NotImplementedError(msg)

            stage_blkts.append(blkt)

            # Parse the decimation if is given.
            decimation_values = set([
                blockette.decimation_correction,
                blockette.decimation_delay, blockette.decimation_factor,
                blockette.decimation_input_sample_rate,
                blockette.decimation_offset])
            if None in decimation_values:
                if len(decimation_values) != 1:
                    msg = ("If a decimation is given, all values must "
                           "be specified.")
                    raise ValueError(msg)
            else:
                blkt = ew.blkt()
                blkt.type = ew.ENUM_FILT_TYPES["DECIMATION"]
                decimation_blkt = blkt.blkt_info.decimation
                decimation_blkt.sample_int = \
                    1.0 / blockette.decimation_input_sample_rate
                decimation_blkt.deci_fact = blockette.decimation_factor
                decimation_blkt.deci_offset = blockette.decimation_offset
                decimation_blkt.estim_delay = blockette.decimation_delay
                decimation_blkt.applied_corr = \
                    blockette.decimation_correction
                stage_blkts.append(blkt)

            # Always add the gain.
            blkt = ew.blkt()
            blkt.type = ew.ENUM_FILT_TYPES["GAIN"]
            gain_blkt = blkt.blkt_info.gain
            gain_blkt.gain = blockette.stage_gain_value
            gain_blkt.gain_freq = blockette.stage_gain_frequency
            stage_blkts.append(blkt)

            if not stage_blkts:
                msg = "At least one blockette is needed for the stage."
                raise ValueError(msg)

            # Attach the blockette chain to the stage.
            st.first_blkt = C.pointer(stage_blkts[0])
            for _i in xrange(1, len(stage_blkts)):
                stage_blkts[_i - 1].next_blkt = C.pointer(stage_blkts[_i])

            stage_objects.append(st)

        chan = ew.channel()
        if not stage_objects:
            msg = "At least one stage is needed."
            raise ValueError(msg)

        # Attach the stage chain to the channel.
        chan.first_stage = C.pointer(stage_objects[0])
        for _i in xrange(1, len(stage_objects)):
            stage_objects[_i - 1].next_stage = C.pointer(stage_objects[_i])

        chan.nstages = len(stage_objects)

        chan.calc_sensit = 0
        chan.sensit = self.instrument_sensitivity.value
        chan.sensfreq = self.instrument_sensitivity.frequency

        fy = 1 / (t_samp * 2.0)
        # start at zero to get zero for offset/ DC of fft
        freqs = np.linspace(0, fy, nfft // 2 + 1).astype("float64")

        output = np.empty(len(freqs), dtype="complex128")
        out_units = C.c_char_p("VEL")

        clibevresp.calc_resp(C.pointer(chan), freqs, len(freqs), output,
                             out_units, -1, 0, 1)
        #output *= scale_factor[0]

        return output, freqs

    def __str__(self):
        ret = (
            "Channel Response\n"
            "\tFrom {input_units} ({input_units_description}) to "
            "{output_units} ({output_units_description})\n"
            "\tOverall Sensitivity: {sensitivity:g} defined at {freq:.3f} Hz\n"
            "\t{stages} stages:\n{stage_desc}").format(
            input_units=self.instrument_sensitivity.input_units,
            input_units_description=self.instrument_sensitivity.
            input_units_description,
            output_units=self.instrument_sensitivity.output_units,
            output_units_description=self.instrument_sensitivity.
            output_units_description,
            sensitivity=self.instrument_sensitivity.value,
            freq=self.instrument_sensitivity.frequency,
            stages=len(self.response_stages),
            stage_desc="\n".join(
                ["\t\tStage %i: %s from %s to %s,"
                 " gain: %.2f" % (
                     i.stage_sequence_number, i.__class__.__name__,
                     i.input_units, i.output_units,
                     i.stage_gain_value)
                 for i in self.response_stages]))
        return ret


class InstrumentSensitivity(ComparingObject):
    """
    From the StationXML Definition:
        The total sensitivity for a channel, representing the complete
        acquisition system expressed as a scalar. Equivalent to SEED stage 0
        gain with (blockette 58) with the ability to specify a frequency range.

    Sensitivity and frequency ranges. The FrequencyRangeGroup is an optional
    construct that defines a pass band in Hertz (FrequencyStart and
    FrequencyEnd) in which the SensitivityValue is valid within the number of
    decibels specified in FrequencyDBVariation.
    """
    def __init__(self, value, frequency, input_units,
                 output_units, input_units_description=None,
                 output_units_description=None, frequency_range_start=None,
                 frequency_range_end=None, frequency_range_DB_variation=None):
        """
        :type value: float
        :param value: Complex type for sensitivity and frequency ranges.
            This complex type can be used to represent both overall
            sensitivities and individual stage gains. The FrequencyRangeGroup
            is an optional construct that defines a pass band in Hertz (
            FrequencyStart and FrequencyEnd) in which the SensitivityValue is
            valid within the number of decibels specified in
            FrequencyDBVariation.
        :type frequency: float
        :param frequency: Complex type for sensitivity and frequency
            ranges.  This complex type can be used to represent both overall
            sensitivities and individual stage gains. The FrequencyRangeGroup
            is an optional construct that defines a pass band in Hertz (
            FrequencyStart and FrequencyEnd) in which the SensitivityValue is
            valid within the number of decibels specified in
            FrequencyDBVariation.
        :param input_units: string
        :param input_units: The units of the data as input from the
            perspective of data acquisition. After correcting data for this
            response, these would be the resulting units.
            Name of units, e.g. "M/S", "V", "PA".
        :param input_units_description: string, optional
        :param input_units_description: The units of the data as input from the
            perspective of data acquisition. After correcting data for this
            response, these would be the resulting units.
            Description of units, e.g. "Velocity in meters per second",
            "Volts", "Pascals".
        :param output_units: string
        :param output_units: The units of the data as output from the
            perspective of data acquisition. These would be the units of the
            data prior to correcting for this response.
            Name of units, e.g. "M/S", "V", "PA".
        :type output_units_description: string, optional
        :param output_units_description: The units of the data as output from
            the perspective of data acquisition. These would be the units of
            the data prior to correcting for this response.
            Description of units, e.g. "Velocity in meters per second",
            "Volts", "Pascals".
        :type frequency_range_start: float, optional
        :param frequency_range_start: Start of the frequency range for which
            the SensitivityValue is valid within the dB variation specified.
        :type frequency_range_end: float, optional
        :param frequency_range_end: End of the frequency range for which the
            SensitivityValue is valid within the dB variation specified.
        :type frequency_range_DB_variation: float, optional
        :param frequency_range_DB_variation: Variation in decibels within the
            specified range.
        """
        self.value = value
        self.frequency = frequency
        self.input_units = input_units
        self.input_units_description = input_units_description
        self.output_units = output_units
        self.output_units_description = output_units_description
        self.frequency_range_start = frequency_range_start
        self.frequency_range_end = frequency_range_end
        self.frequency_range_DB_variation = frequency_range_DB_variation


# XXX duplicated code, PolynomialResponseStage could probably be implemented by
# XXX inheriting from both InstrumentPolynomial and ResponseStage
class InstrumentPolynomial(ComparingObject):
    """
    From the StationXML Definition:
        The total sensitivity for a channel, representing the complete
        acquisition system expressed as a polynomial. Equivalent to SEED stage
        0 polynomial (blockette 62).
    """
    def __init__(self, input_units, output_units,
                 resource_id, name, frequency_lower_bound,
                 frequency_upper_bound, approximation_lower_bound,
                 approximation_upper_bound, maximum_error, coefficients,
                 approximation_type='MACLAURIN',
                 input_units_description=None,
                 output_units_description=None, description=None):
        """
        :type approximation_type: str
        :param approximation_type: Approximation type. Currently restricted to
            'MACLAURIN' by StationXML definition.
        :type frequency_lower_bound: float
        :param frequency_lower_bound: Lower frequency bound.
        :type frequency_upper_bound: float
        :param frequency_upper_bound: Upper frequency bound.
        :type approximation_lower_bound: float
        :param approximation_lower_bound: Lower bound of approximation.
        :type approximation_upper_bound: float
        :param approximation_upper_bound: Upper bound of approximation.
        :type maximum_error: float
        :param maximum_error: Maximum error.
        :type coefficients: list of floats
        :param coefficients: List of polynomial coefficients.
        :param input_units: string
        :param input_units: The units of the data as input from the
            perspective of data acquisition. After correcting data for this
            response, these would be the resulting units.
            Name of units, e.g. "M/S", "V", "PA".
        :param output_units: string
        :param output_units: The units of the data as output from the
            perspective of data acquisition. These would be the units of the
            data prior to correcting for this response.
            Name of units, e.g. "M/S", "V", "PA".
        :type resource_id: string
        :param resource_id: This field contains a string that should serve as a
            unique resource identifier. This identifier can be interpreted
            differently depending on the datacenter/software that generated the
            document. Also, we recommend to use something like
            GENERATOR:Meaningful ID. As a common behaviour equipment with the
            same ID should contains the same information/be derived from the
            same base instruments.
        :type name: string
        :param name: A name given to the filter stage.
        :param input_units_description: string, optional
        :param input_units_description: The units of the data as input from the
            perspective of data acquisition. After correcting data for this
            response, these would be the resulting units.
            Description of units, e.g. "Velocity in meters per second",
            "Volts", "Pascals".
        :type output_units_description: string, optional
        :param output_units_description: The units of the data as output from
            the perspective of data acquisition. These would be the units of
            the data prior to correcting for this response.
            Description of units, e.g. "Velocity in meters per second",
            "Volts", "Pascals".
        :type description: string, optional
        :param description: A short description of of the filter.
        """
        self.input_units = input_units
        self.output_units = output_units
        self.input_units_description = input_units_description
        self.output_units_description = output_units_description
        self.resource_id = resource_id
        self.name = name
        self.description = description
        self._approximation_type = approximation_type
        self.frequency_lower_bound = frequency_lower_bound
        self.frequency_upper_bound = frequency_upper_bound
        self.approximation_lower_bound = approximation_lower_bound
        self.approximation_upper_bound = approximation_upper_bound
        self.maximum_error = maximum_error
        self.coefficients = coefficients

    @property
    def approximation_type(self):
        return self._approximation_type

    @approximation_type.setter
    def approximation_type(self, value):
        value = str(value).upper()
        allowed = ("MACLAURIN",)
        if value not in allowed:
            msg = ("Value '%s' for polynomial response approximation type not "
                   "allowed. Possible values are: '%s'")
            msg = msg % (value, "', '".join(allowed))
            raise ValueError(msg)
        self._approximation_type = value


if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
